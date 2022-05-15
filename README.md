# Graph Prime Calculator

Graph Prime Calculator is a cross-platform prime number calculator developed on Tauri to simultaneously allow beautiful graphs, excellent performance, and code-sharing between platforms. The frontend "framework" of choice is Svelte for simplicity's sake.
![Screenshot on Linux Fedora](https://user-images.githubusercontent.com/37254797/168457911-50231971-90e5-446f-880a-5e379304db09.png)

The web view displays the beautiful SVG graphs generated by frappe while the whole calculation runs on the excellent-performing rust backend. The application is currently available for all desktop platforms and will be available for the web and mobile as soon as Tauri enables those options. Download the latest build through GitHub releases here: https://github.com/DoodlesEpic/GraphPrime/releases/latest.

## Developing

### Get started

Read the Tauri documentation to check how to run the project
https://tauri.studio/v1/guides/development/development-cycle

### Testing

To start developing, run:

```bash
npm install
```

and then you can start the Tauri dev server:

```bash
npm run tauri dev
```

You need to have Rust and NodeJS ready to run on your system before doing this
https://tauri.studio/v1/guides/getting-started/prerequisites/

## License

This project is licensed under the GNU GPL v3 free software license. Read the LICENSE file for more information.
