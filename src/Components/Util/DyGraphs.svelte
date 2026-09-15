<svelte:options runes={true} />

<script lang="ts">
  import Dygraph from "dygraphs";

  let {
    options = {
      data: "",
      fullscreen: false
    },
    class: classes = ""
  }: {
    options: { data: string; fullscreen: boolean };
    class?: string;
  } = $props();

  let element: HTMLElement;

  $effect(() => {
    void options;
    if (element) {
      const graph = new Dygraph(element, options.data, {});
      return () => graph.destroy();
    }
  });
</script>

<div bind:this={element} class={classes}></div>

<style>
  .chart {
    position: absolute;
    inset: 100px 10px 10px 10px;
  }
</style>
