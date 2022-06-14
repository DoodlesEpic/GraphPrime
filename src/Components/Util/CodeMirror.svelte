<script lang="ts">
  import { onMount } from "svelte";
  import { EditorView, minimalSetup } from "codemirror";

  export let primes: number[];
  export let editorFullscreen: boolean;

  let view: EditorView;
  let element: HTMLElement;

  onMount(() => {
    createEditor();
  });

  $: if (primes) {
    setEditorText();
  }

  $: maximumHeightEditor = EditorView.theme({
    "&": { maxHeight: editorFullscreen ? "calc(100vh - 150px)" : "300px" },
    ".cm-scroller": { overflow: "auto" },
  });

  // This is a hack to get the editor to resize itself when fullscreen
  // It would be nicer if we could just change the theme, but I couldn't find a way to do that
  $: if (editorFullscreen || !editorFullscreen) {
    createEditor();
    setEditorText();
  }

  function createEditor() {
    if (view) element.innerHTML = "";
    view = new EditorView({
      parent: element,
      extensions: [minimalSetup, maximumHeightEditor, EditorView.lineWrapping],
    });
  }

  function setEditorText() {
    if (view) {
      view.dispatch(
        view.state.update({
          changes: {
            from: 0,
            to: view.state.doc.length,
            insert: primes.join(", "),
          },
        })
      );
    }
  }
</script>

<div bind:this={element} />
