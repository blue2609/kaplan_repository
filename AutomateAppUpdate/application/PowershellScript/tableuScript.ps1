param($version,$activationKey,$register,$autoUpdate)
$installArguments = "'ACTIVATE_KEY=" + "`"$activationKey`"" + " REGISTER=$register AUTOUPDATE=$autoUpdate'"
choco install `
        'Tableau-Desktop' `
        --version=$version `
        --yes `
        --allowmultipleversions `
        --ia=$installArguments