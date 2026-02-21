<svelte:options runes={true} />

<script lang="ts">
  import { onMount } from "svelte";
  import { EditorView, minimalSetup } from "codemirror";

  let {
    primes = $bindable(),
    editorFullscreen = $bindable()
  }: {
    primes: number[];
    editorFullscreen: boolean;
  } = $props();

  let view: EditorView | undefined;
  let element: HTMLElement;

  const maximumHeightEditor = $derived(
    EditorView.theme({
      "&": { maxHeight: editorFullscreen ? "calc(100vh - 150px)" : "300px" },
      ".cm-scroller": { overflow: "auto" }
    })
  );

  onMount(() => {
    createEditor();
    return () => view?.destroy();
  });

  $effect(() => {
    void primes;
    setEditorText();
  });

  $effect(() => {
    void editorFullscreen;
    if (element) {
      createEditor();
      setEditorText();
    }
  });

  function createEditor() {
    if (view) view.destroy();
    view = new EditorView({
      parent: element,
      extensions: [minimalSetup, maximumHeightEditor, EditorView.lineWrapping]
    });
  }

  function setEditorText() {
    if (view) {
      view.dispatch(
        view.state.update({
          changes: {
            from: 0,
            to: view.state.doc.length,
            insert: primes.join(", ")
          }
        })
      );
    }
  }
</script>

<div bind:this={element}></div>
