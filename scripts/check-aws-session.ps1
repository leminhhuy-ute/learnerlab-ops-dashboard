[CmdletBinding()]
param(
    [ValidateSet('us-east-1', 'us-west-2')]
    [string]$Region = 'us-east-1',
    [string]$Profile,
    [ValidatePattern('^[a-zA-Z][a-zA-Z0-9-]*$')]
    [ValidateLength(1, 128)]
    [string]$StackName,
    [ValidatePattern('^\d{12}$')]
    [string]$ExpectedAccountId
)

$ErrorActionPreference = 'Stop'
$awsCommand = Get-Command aws -ErrorAction SilentlyContinue
if (-not $awsCommand) {
    throw 'AWS CLI was not found. Install AWS CLI v2, then open a new PowerShell session. No AWS action was performed.'
}

$commonArguments = @('--region', $Region, '--no-cli-pager')
if ($Profile) { $commonArguments += @('--profile', $Profile) }

function Invoke-AwsRead {
    param([string[]]$Arguments)
    $savedPreference = $ErrorActionPreference
    try {
        # Windows PowerShell turns native stderr into ErrorRecord objects.
        $ErrorActionPreference = 'Continue'
        $raw = & $awsCommand @Arguments @commonArguments 2>&1
        $awsExitCode = $LASTEXITCODE
    }
    finally { $ErrorActionPreference = $savedPreference }
    if ($awsExitCode -ne 0) {
        $message = ($raw | ForEach-Object { $_.ToString() }) -join [Environment]::NewLine
        throw "AWS read failed ($($Arguments[0]) $($Arguments[1])). $message"
    }
    return (($raw | ForEach-Object { $_.ToString() }) -join [Environment]::NewLine)
}

$identity = Invoke-AwsRead -Arguments @('sts', 'get-caller-identity', '--output', 'json') | ConvertFrom-Json
if ($ExpectedAccountId -and $identity.Account -ne $ExpectedAccountId) {
    throw "Wrong account. Expected $ExpectedAccountId; connected to $($identity.Account)."
}

$labRoleArn = Invoke-AwsRead -Arguments @('iam', 'get-role', '--role-name', 'LabRole', '--query', 'Role.Arn', '--output', 'text')
if ($labRoleArn -ne "arn:aws:iam::$($identity.Account):role/LabRole") {
    throw 'Existing LabRole has an unexpected ARN. Check that the credentials belong to AWS Learner Lab.'
}

$labInstanceProfileArn = $null
try {
    $labInstanceProfileArn = Invoke-AwsRead -Arguments @('iam', 'get-instance-profile', '--instance-profile-name', 'LabInstanceProfile', '--query', 'InstanceProfile.Arn', '--output', 'text')
}
catch {
    Write-Warning 'LabInstanceProfile could not be read. It is optional for week 1 because this template creates no EC2 instance.'
}

$checkedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
Write-Host "Account ID: $($identity.Account)"
Write-Host "Region: $Region"
Write-Host "Checked at UTC: $checkedAtUtc"
Write-Host "Caller ARN: $($identity.Arn)"
Write-Host "Existing LabRole: $labRoleArn"
if ($labInstanceProfileArn) { Write-Host "Existing LabInstanceProfile: $labInstanceProfileArn" }

$artifactBucketName = $null
if ($StackName) {
    $stack = Invoke-AwsRead -Arguments @('cloudformation', 'describe-stacks', '--stack-name', $StackName, '--query', 'Stacks[0]', '--output', 'json') | ConvertFrom-Json
    if ($stack.StackStatus -notin @('CREATE_COMPLETE', 'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_COMPLETE')) {
        throw "Stack is not ready for verification: $($stack.StackStatus)"
    }
    $bucketOutput = @($stack.Outputs | Where-Object { $_.OutputKey -eq 'ArtifactBucketName' })
    if ($bucketOutput.Count -ne 1) { throw 'ArtifactBucketName output was not found in the stack.' }
    $artifactBucketName = $bucketOutput[0].OutputValue
    $publicBlock = Invoke-AwsRead -Arguments @('s3api', 'get-public-access-block', '--bucket', $artifactBucketName, '--query', 'PublicAccessBlockConfiguration', '--output', 'json') | ConvertFrom-Json
    foreach ($key in @('BlockPublicAcls', 'IgnorePublicAcls', 'BlockPublicPolicy', 'RestrictPublicBuckets')) {
        if ($publicBlock.$key -ne $true) { throw "S3 public access block is disabled: $key" }
    }
    $algorithm = Invoke-AwsRead -Arguments @('s3api', 'get-bucket-encryption', '--bucket', $artifactBucketName, '--query', 'ServerSideEncryptionConfiguration.Rules[0].ApplyServerSideEncryptionByDefault.SSEAlgorithm', '--output', 'text')
    if ($algorithm -ne 'AES256') { throw 'Expected S3 encryption algorithm AES256.' }
    $bucketRegion = Invoke-AwsRead -Arguments @('s3api', 'get-bucket-location', '--bucket', $artifactBucketName, '--query', 'LocationConstraint', '--output', 'json') | ConvertFrom-Json
    if ($null -eq $bucketRegion) { $bucketRegion = 'us-east-1' }
    if ($bucketRegion -ne $Region) { throw "Bucket region mismatch: $bucketRegion" }
    $bucketTags = Invoke-AwsRead -Arguments @('s3api', 'get-bucket-tagging', '--bucket', $artifactBucketName, '--query', 'TagSet', '--output', 'json') | ConvertFrom-Json
    foreach ($key in @('Project', 'Owner', 'Environment')) {
        $matchingTags = @($bucketTags | Where-Object { $_.Key -eq $key -and $_.Value })
        if ($matchingTags.Count -ne 1) { throw "S3 tag missing or empty: $key" }
    }
    Write-Host "Stack verified: $StackName ($($stack.StackStatus))"
    Write-Host "Private encrypted S3 bucket: $artifactBucketName"
}

# Only identifiers/status are returned. Access keys and session tokens are never read or printed.
[pscustomobject]@{
    AccountId = $identity.Account
    Region = $Region
    CheckedAtUtc = $checkedAtUtc
    CallerArn = $identity.Arn
    LabRoleArn = $labRoleArn
    LabInstanceProfileArn = $labInstanceProfileArn
    StackName = $StackName
    ArtifactBucketName = $artifactBucketName
}
