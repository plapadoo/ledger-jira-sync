let
  bootstrap = import <nixpkgs> { };

  nixpkgs = builtins.fromJSON (builtins.readFile ./nixpkgs.json);

  src = bootstrap.fetchFromGitHub {
    owner = "NixOS";
    repo  = "nixpkgs-channels";
    inherit (nixpkgs) rev sha256;
  };

  pkgs = import src { };

  pythonPkgs = pkgs.python27Packages;

  jira-python = pythonPkgs.buildPythonPackage rec {
    pname = "jira";
    version = "2.0.0";
    doCheck = false;

    src = pythonPkgs.fetchPypi {
      inherit pname version;
      sha256 = "14qfpbnjnmqz44zk0msdgpx39ary21vdq2h3xnfv4icfz7glmag2";
    };

  buildInputs = [
    pythonPkgs.sphinx
    pythonPkgs.pytestrunner
    pythonPkgs.pbr
    pythonPkgs.ordereddict
    pythonPkgs.argparse
    pythonPkgs.requests_oauthlib
    pythonPkgs.requests_toolbelt
    pythonPkgs.defusedxml
  ];

  propagatedBuildInputs = [
    pythonPkgs.ordereddict
    pythonPkgs.requests_oauthlib
    pythonPkgs.requests_toolbelt
    pythonPkgs.ipython
    pythonPkgs.defusedxml
    pythonPkgs.pbr
  ];
  };
in
  pythonPkgs.buildPythonApplication rec {
    name = "ledger-jira-sync";
    version = "1.0";
    src = ./.;
    # So nix-shell contains the Python path
    shellHook = "export PYTHONPATH=$(pwd):$PYTHONPATH";
    propagatedBuildInputs = [
      jira-python
      pkgs.ledger
    ];
    checkPhase = ''
      PYLINTHOME="/tmp" pylint ledger_jira_sync
    '';
    
    checkInputs = [ pythonPkgs.pylint ];

    buildInputs = [
      pkgs.python2
      pythonPkgs.ipdb

      # only for IDE features
      pythonPkgs.autopep8
    ];
}
