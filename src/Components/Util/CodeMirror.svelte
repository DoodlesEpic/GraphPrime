<!-- 
    Adapted from https://svelte.dev/repl/a199ca2d451e4b0b92a8abd2d0e71ec6?version=3.35.0
    As an alternative to @joshnuss/svelte-codemirror
    Removed a lot of unnecessary code from the original example, specifically the styling
 -->
<script lang="ts">
  import { onMount } from "svelte";
  import { EditorView, minimalSetup } from "codemirror";

  export let primes: number[];

  let view;
  let element: HTMLElement;

  onMount(() => {
    createEditor();
  });

  $: if (primes) {
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

  const maximumHeightEditor = EditorView.theme({
    "&": { maxHeight: "400px" },
    ".cm-scroller": { overflow: "auto" },
  });

  function createEditor() {
    if (view) element.innerHTML = "";
    view = new EditorView({
      parent: element,
      extensions: [minimalSetup, maximumHeightEditor, EditorView.lineWrapping],
    });
  }
</script>

<div bind:this={element} />
