<script>
  import { onMount } from "svelte";
  import Dygraph from "dygraphs";
  import "dygraph.css";

  let classes = "";

  export let graph = null;
  export let options = {
    data: "",
    fullscreen: false,
  };
  export { classes as class };

  let element;

  onMount(() => {
    createGraph();
  });

  $: if (element && options) {
    createGraph();
  }

  function createGraph() {
    if (graph) element.innerHTML = "";
    graph = new Dygraph(element, options.data, {});
  }
</script>

<div bind:this={element} class={classes} />

<style>
  .chart {
    position: absolute;
    inset: 100px 10px 10px 10px;
  }
</style>
