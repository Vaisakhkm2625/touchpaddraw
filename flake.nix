{
  description = "Nix shell with Python and evdev";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs";

  outputs = { nixpkgs, ... }: 
  let
    pkgs = nixpkgs.legacyPackages.x86_64-linux;
  in {
    devShells.x86_64-linux.default = pkgs.mkShell {
      buildInputs = [
        pkgs.python3
        pkgs.python3Packages.evdev
        pkgs.dotool
      ];
    };
  };
}
