{
  description = "A development environment with astral uv";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        # Development shell: `nix develop`
        devShells.default = pkgs.mkShell {
          buildInputs = [
            pkgs.uv
          ];

          shellHook = ''
            echo "uv $(uv --version)"
          '';
        };

        # Standalone package: `nix build` / `nix run`
        packages.default = pkgs.uv;

        # Run directly: `nix run`
        apps.default = {
          type = "app";
          program = "${pkgs.uv}/bin/uv";
        };
      }
    );
}
