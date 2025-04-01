{
  description = "Nix flake with Python and evdev, runnable via nix run";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs";

  outputs = { self, nixpkgs, ... }:
  let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
  in {
    devShells.${system}.default = pkgs.mkShell {
      buildInputs = [
        pkgs.python3
        pkgs.python3Packages.evdev
        pkgs.dotool
      ];
    };

    packages.${system}.default = pkgs.python3Packages.buildPythonPackage {
      pname = "touchpaddraw";
      version = "0.1.0";
      src = ./.;
      format = "other";
      propagatedBuildInputs = [
        pkgs.python3Packages.evdev
        pkgs.dotool
      ];
      installPhase = ''
        mkdir -p $out/bin
        cp main.py $out/bin/main.py
        cp dotoolc.py $out/bin/dotoolc.py
        chmod +x $out/bin/main.py
      '';
    };

    apps.${system}.default = {
      type = "app";
      program = "${self.packages.${system}.default}/bin/main.py";
    };
  };
}
