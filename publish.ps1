Write-Host "Starting publish." -ForegroundColor Green

# Push version number
Write-Host "`nPushing version number" -ForegroundColor Yellow
Write-Host "About to run Python script..."
python push_version.py
Write-Host "Python script completed."
Write-Host "Exit code: $LASTEXITCODE"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to push version number." -ForegroundColor Red
    exit 1
}
Write-Host "Continuing after version push..." -ForegroundColor Green

# Build the package
Write-Host "`nBuilding the package" -ForegroundColor Yellow
poetry build
if ($LASTEXITCODE -ne 0) {
    Write-Host "Package build failed." -ForegroundColor Red
    exit 1
}

# Check if environment variables are set
if (-not ${env:pypi-username}) {
    Write-Host "PyPI username not set. Please set environment variable pypi-username." -ForegroundColor Red
    exit 1
}
if (-not ${env:pypi-password}) {
    Write-Host "PyPI password not set. Please set environment variable pypi-password." -ForegroundColor Red
    exit 1
}

# Publish to PyPI
Write-Host "`nPublishing to PyPI" -ForegroundColor Yellow
poetry publish --username ${env:pypi-username} --password ${env:pypi-password}
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to publish to PyPI." -ForegroundColor Red
    exit 1
}

# Commit and push changes to GitHub
Write-Host "`nPushing to Github." -ForegroundColor Yellow
git add .
git commit -m "version bump"
git push
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to push to GitHub." -ForegroundColor Red
    exit 1
}

Write-Host "`nPublish complete." -ForegroundColor Green
# SIG # Begin signature block
# MIIFcwYJKoZIhvcNAQcCoIIFZDCCBWACAQExCzAJBgUrDgMCGgUAMGkGCisGAQQB
# gjcCAQSgWzBZMDQGCisGAQQBgjcCAR4wJgIDAQAABBAfzDtgWUsITrck0sYpfvNR
# AgEAAgEAAgEAAgEAAgEAMCEwCQYFKw4DAhoFAAQUM8dKByJzaIYG4ylNpwoDZzz+
# k6ugggMMMIIDCDCCAfCgAwIBAgIQeHX/w0b4Z7ZOUpxJKOaiATANBgkqhkiG9w0B
# AQsFADAcMRowGAYDVQQDDBFNeUNvZGVTaWduaW5nQ2VydDAeFw0yNTA1MTAxNTE4
# NTVaFw0yNjA1MTAxNTM4NTVaMBwxGjAYBgNVBAMMEU15Q29kZVNpZ25pbmdDZXJ0
# MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuV24mKy4ZHc4DcbYJ4d0
# +Zp3+xMG6sBMdLqgyGujKE3d9o37jPSa/oGTbXGGw23+1qWZP9tr22PbyFHSqFz1
# 8SafzfTLIZukfC9ba2o6e1pOJ++JNGLomLtQNoyZmoo0sSDc8Xm9hyC2UQBViPPB
# OmXrczxwZWYuuEZS7Hzm7WV9uvXPF9/lY3bmNBQV3O8L4a2jicoGpiBMgcHNnq25
# 34/iDYd/ztHaOPvajJHEnRVeSoLIYo5/7RB84MktLxHf69H2nIvh24hALEbPeAYc
# x5iNNoMNTf1S7gbKWDDc1QFucpzfdz9N2M+4diwLkcbSBEsDhE7rXHE1Ml72/MhR
# lQIDAQABo0YwRDAOBgNVHQ8BAf8EBAMCB4AwEwYDVR0lBAwwCgYIKwYBBQUHAwMw
# HQYDVR0OBBYEFCZ5Cl2xpLrYcF6xE8iGJtq5vRJtMA0GCSqGSIb3DQEBCwUAA4IB
# AQADf1Z6BWwXbt290stuERVufCpfJvi+HjVdfI6SGMRRoUVDYe5vnkyEcDbR0kcR
# RAqNlmJ4NRg5fh+ngJSVXmsexEWlGb33zQCD3ENoTMZYKKL9SNgGm6knDsCPpkF2
# xiQodNVupPgJQbfHW1bU/xseKmjKWD2wU2CEyU/EHUD0nWPV0A3coRML2Pyq6d+2
# NCDjOLd0+SD3AI44Su0nbe8L22+98RnXxg5NspNQmFfur4vmiQTfoVNkOg8IKrup
# 33Rln1DGmtxaXeGAHCGsvXib3Hpw3B1TOBV+/WkUji7t+HzYglxe2JwB2xHrIB9v
# XFsTZViNZ0qTV9lrZDIjAgLPMYIB0TCCAc0CAQEwMDAcMRowGAYDVQQDDBFNeUNv
# ZGVTaWduaW5nQ2VydAIQeHX/w0b4Z7ZOUpxJKOaiATAJBgUrDgMCGgUAoHgwGAYK
# KwYBBAGCNwIBDDEKMAigAoAAoQKAADAZBgkqhkiG9w0BCQMxDAYKKwYBBAGCNwIB
# BDAcBgorBgEEAYI3AgELMQ4wDAYKKwYBBAGCNwIBFTAjBgkqhkiG9w0BCQQxFgQU
# 7BNiKZCQZtt5CeWJbYvE55a9kdUwDQYJKoZIhvcNAQEBBQAEggEAAyQOxJcqusMu
# uHyYJRI6xRTLwIV3V6+efgxwm5sD/41VVZnTkRdG4Ay2ldfx92VFY703oKddP2Fb
# k+IfXocNsPOHZacrIqOG4arNkqyMrIUH+EdG70TMQP2XU5NF9GuASfvryqlX5gko
# tMwVMk8W5rxXU6wtzX6Yr84bwtsEaciNS9/iOVvKZX1B3uo48zSlY0SSB+9gddT1
# cduM5jCeF6+b1mbSkZx0uQeglIsumDCFD7wKxe2+g36sVVTG4UGlXaE1ldZuWcQx
# FCwAfhGaqjpgoRT8GDnFAOJAUdN6VyB8moqRfR2sobW6/g207ZTv5YDqbPIX341E
# et/7yE9MkA==
# SIG # End signature block
