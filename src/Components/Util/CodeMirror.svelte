<!-- 
    Adapted from https://svelte.dev/repl/a199ca2d451e4b0b92a8abd2d0e71ec6?version=3.35.0
    As an alternative to @joshnuss/svelte-codemirror
    Removed a lot of unnecessary code from the original example, specifically the styling
 -->
<script lang="ts">
  import { onMount } from "svelte";
  import { EditorView } from "@codemirror/view";
  import { EditorState } from "@codemirror/state";

  export let primes: number[];

  let view;
  let element: HTMLElement;

  onMount(() => {
    createEditor();
  });

  $: if (element && primes) {
    createEditor();
  }

  function createEditor() {
    if (view) element.innerHTML = "";
    view = new EditorView({
      parent: element,
      state: EditorState.create({
        doc: primes.join(", "),
      }),
    });
  }
</script>

<div bind:this={element} />
