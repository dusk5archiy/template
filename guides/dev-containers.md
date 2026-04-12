# Using devcontainer files in VS Code

## Applied to

- VS Code
- WSL

## Prerequisites

- WSL with Docker installed
- VS Code with `Dev Containers` extension.
- (Optional) In WSL, enable forwarding GPU into containers.

## Setup


## How to

### Enter a dev container

In your project root folder, create a new folder called `.devcontainer`,
then create `devcontainer.json` inside the folder with appropriate contents.

After that, press CTRL+SHIFT+P and choose `Dev Containers: Reopen in Container`.

### Folder mounts

```json
{
  "mounts": [
    "source=<|A|>,target=<|B|>,type=bind,consistency=cached"
  ],
}
```

- `A`: Your source folder in WSL.
- `B`: Target folder in the container, automatically created if not exists.

### Running commands after creating the container

```json
{
  "postCreateCommand": "<|command|>",
}
```
