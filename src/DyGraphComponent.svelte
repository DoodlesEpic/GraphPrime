<script>
  import { onMount } from "svelte";
  import Dygraph from "dygraphs";
  import "dygraph.css";

  let classes = "";

  export let graph = null;
  export let data;
  export { classes as class };

  let element;

  onMount(() => {
    createGraph();
  });

  $: if (element && data) {
    createGraph();
  }

  function createGraph() {
    if (graph) element.innerHTML = "";
    graph = new Dygraph(element, data, {});
  }
</script>

<div bind:this={element} class={classes} />

<style unscoped></style>
