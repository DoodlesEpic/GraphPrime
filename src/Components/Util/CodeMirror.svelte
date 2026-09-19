<script lang="ts">
  import { onMount } from "svelte";
  import { EditorView, minimalSetup } from "codemirror";

  let { primes, editorFullscreen }: { primes: number[]; editorFullscreen: boolean } = $props();
  let element: HTMLDivElement;
  let view = $state.raw<EditorView>();

  onMount(() => {
    const editor = new EditorView({
      parent: element,
      extensions: [minimalSetup, EditorView.lineWrapping]
    });
    view = editor;
    return () => editor.destroy();
  });

  $effect(() => {
    view?.dispatch({
      changes: { from: 0, to: view.state.doc.length, insert: primes.join(", ") }
    });
  });
</script>

<div
  bind:this={element}
  style:--editor-height={editorFullscreen ? "calc(100vh - 150px)" : "300px"}
></div>

<style>
  div :global(.cm-editor) {
    max-height: var(--editor-height);
  }
  div :global(.cm-scroller) {
    overflow: auto;
  }
</style>
