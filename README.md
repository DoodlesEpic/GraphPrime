# Graph Prime Calculator

![GPL v3 License](https://img.shields.io/github/license/DoodlesEpic/GraphPrime)
![Build Status Badge](https://img.shields.io/github/actions/workflow/status/DoodlesEpic/GraphPrime/.github/workflows/main.yml?branch=main)
![Supported on all desktop platforms badge](https://img.shields.io/badge/platforms-windows%2C%20macos%2C%20linux-informational)
![Code Size Badge](https://img.shields.io/github/languages/code-size/DoodlesEpic/GraphPrime)
![Lines of Code Badge](https://img.shields.io/tokei/lines/github/DoodlesEpic/GraphPrime)
![Release Version Badge](https://img.shields.io/github/v/release/DoodlesEpic/GraphPrime)
![Downloads Badge](https://img.shields.io/github/downloads/DoodlesEpic/GraphPrime/total)

Graph Prime Calculator is a cross-platform prime number calculator developed on Tauri to simultaneously allow beautiful graphs, excellent performance, and code-sharing between platforms. The frontend "framework" of choice is Svelte for simplicity's sake.
![Screenshot on Linux Fedora](https://user-images.githubusercontent.com/37254797/168457911-50231971-90e5-446f-880a-5e379304db09.png)

The web view displays the beautiful SVG graphs generated by frappe and dygraphs while the whole calculation runs on the excellent-performing rust backend. The application is currently available for all desktop platforms and will be available for the web and mobile as soon as Tauri enables those options.

## Get started

### Download

Download the latest build through GitHub releases here: https://github.com/DoodlesEpic/GraphPrime/releases/latest. Updates are fetched automatically by the program.

### Screenshots

![Screenshot from 2022-06-19 00-02-03](https://user-images.githubusercontent.com/37254797/174464122-88aa1a35-174e-4e54-a772-ff7a0da881f6.png)
![Screenshot from 2022-06-19 00-02-13](https://user-images.githubusercontent.com/37254797/174464124-558b5898-be9b-476b-9921-7a98a9622df3.png)

#### Dark mode

![Screenshot from 2022-07-17 21-46-52](https://user-images.githubusercontent.com/37254797/179431795-d7f6c59d-cbd1-4bf3-9762-cc69c684126b.png)
![Screenshot from 2022-07-17 21-47-53](https://user-images.githubusercontent.com/37254797/179431799-aa08eb33-7c88-4803-af0a-83c13e403929.png)

## Developers

### Get started

Read the Tauri documentation to check how to run the project
https://tauri.studio/v1/guides/development/development-cycle

### Testing

To start developing, run:

```bash
yarn
```

and then you can start the Tauri dev server:

```bash
yarn run tauri dev
```

You need to have Rust and NodeJS ready to run on your system before doing this
https://tauri.studio/v1/guides/getting-started/prerequisites/

The Yarn version being used is berry. If you don't have Yarn v4 in your system, you can enable it with:

```bash
corepack enable
```

### Deployment

Before creating a new release update the semver versions on the package.json, cargo.toml, tauri.conf.json, _run a build_ and _run yarn install_ as that will update both package manager lockfiles. Deployment of new versions is done by creating a new semver versioned tag and pushing it to GitHub, this will automatically trigger the [Tauri Action CI](https://github.com/tauri-apps/tauri-action) to start a new build and create a new release. It's important that the build environment contains the updater private key or else the build will fail.

After the release has been published with the appropiate change notes, build artifacts and update signatures the final step is to update the [GitHub Gist with the current version information](https://gist.githubusercontent.com/DoodlesEpic/e19632f3fe451cd9a14f9322880d8ebf/raw/6ac23f0bbc0b6f798897a9fec8ae86237577c8c8/GraphPrimeUpdater.json) at https://gist.github.com/DoodlesEpic/e19632f3fe451cd9a14f9322880d8ebf as that is where the updater looks at to see what is the latest version of the software.

## License

This project is licensed under the GNU GPL v3 free software license. Read the LICENSE file for more information.
