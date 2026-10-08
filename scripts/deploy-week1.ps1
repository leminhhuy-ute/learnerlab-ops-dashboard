[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[A-Za-z0-9_.@:/+=-]+$')]
    [ValidateLength(1, 80)]
    [string]$Owner,
    [ValidatePattern('^[A-Za-z0-9_.@:/+=-]+$')]
    [ValidateLength(1, 80)]
    [string]$Project = 'learnerlab-ops',
    [ValidateSet('learner-lab')]
    [string]$Environment = 'learner-lab',
    [ValidateSet('us-east-1', 'us-west-2')]
    [string]$Region = 'us-east-1',
    [ValidatePattern('^[a-zA-Z][a-zA-Z0-9-]*$')]
    [ValidateLength(1, 128)]
    [string]$StackName = 'learnerlab-ops-week1',
    [string]$Profile,
    [ValidatePattern('^\d{12}$')]
    [string]$ExpectedAccountId,
    [switch]$Execute
)

$ErrorActionPreference = 'Stop'
$templatePath = Join-Path (Join-Path (Split-Path $PSScriptRoot -Parent) 'infra') 'week1-foundation.yaml'
if (-not (Test-Path -LiteralPath $templatePath -PathType Leaf)) { throw "Missing template: $templatePath" }

$sessionArguments = @{Region = $Region}
if ($Profile) { $sessionArguments.Profile = $Profile }
if ($ExpectedAccountId) { $sessionArguments.ExpectedAccountId = $ExpectedAccountId }
$session = & (Join-Path $PSScriptRoot 'check-aws-session.ps1') @sessionArguments
$awsCommand = Get-Command aws -ErrorAction Stop
$commonArguments = @('--region', $Region, '--no-cli-pager')
if ($Profile) { $commonArguments += @('--profile', $Profile) }

function Invoke-AwsChecked {
    param([string[]]$Arguments)
    $savedPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = 'Continue'
        $raw = & $awsCommand @Arguments @commonArguments 2>&1
        $awsExitCode = $LASTEXITCODE
    }
    finally { $ErrorActionPreference = $savedPreference }
    if ($awsExitCode -ne 0) {
        $message = ($raw | ForEach-Object { $_.ToString() }) -join [Environment]::NewLine
        throw "AWS CLI failed ($($Arguments[0]) $($Arguments[1])). $message"
    }
    return (($raw | ForEach-Object { $_.ToString() }) -join [Environment]::NewLine)
}

$null = Invoke-AwsChecked -Arguments @('cloudformation', 'validate-template', '--template-body', "file://$templatePath", '--output', 'json')
Write-Host "Template accepted by AWS CloudFormation in account $($session.AccountId), region $Region."
Write-Host "Tags: Project=$Project, Owner=$Owner, Environment=$Environment"

$deployArguments = @(
    'cloudformation', 'deploy', '--template-file', $templatePath,
    '--stack-name', $StackName,
    '--parameter-overrides', "Project=$Project", "Owner=$Owner", "Environment=$Environment",
    '--tags', "Project=$Project", "Owner=$Owner", "Environment=$Environment",
    '--no-fail-on-empty-changeset'
)
if (-not $Execute) { $deployArguments += '--no-execute-changeset' }

# Uses the caller's temporary Learner Lab credentials. It does not create or
# modify IAM roles and does not require passing LabRole to CloudFormation.
$deployOutput = Invoke-AwsChecked $deployArguments
if ($deployOutput) { Write-Host $deployOutput }

if ($Execute) {
    $sessionArguments.StackName = $StackName
    $null = & (Join-Path $PSScriptRoot 'check-aws-session.ps1') @sessionArguments
    Write-Host 'Week 1 foundation deployed and checked. The S3 bucket is retained when this stack is deleted.'
}
else {
    Write-Host 'CloudFormation change set created for review; its resources have not been provisioned.'
    Write-Host 'Use the same command with -Execute to create/update the foundation.'
    Write-Host "Review console: https://$Region.console.aws.amazon.com/cloudformation/home?region=$Region#/stacks"
}
