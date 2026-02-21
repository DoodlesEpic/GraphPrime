<svelte:options runes={true} />

<script lang="ts">
  let { chartType = $bindable() }: { chartType: string } = $props();
</script>

<div class="graphTypeSwitch">
  <select name="Graph Types" class="graphTypes" bind:value={chartType} aria-label="Graph type">
    <option value="frappe">Basic</option>
    <option value="dygraph">Scientific</option>
  </select>
</div>

<style>
  .graphTypeSwitch {
    position: absolute;
    left: 10px;
    top: 10px;
  }

  .graphTypes {
    min-width: 120px;
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 0.3rem 2rem 0.3rem 0.6rem;
    font-size: 0.95rem;
    color: var(--body-color);
    background-color: var(--card-bg);
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    background-image:
      linear-gradient(45deg, transparent 50%, currentColor 50%),
      linear-gradient(135deg, currentColor 50%, transparent 50%);
    background-position:
      calc(100% - 14px) calc(50% + 1px),
      calc(100% - 9px) calc(50% + 1px);
    background-size:
      5px 5px,
      5px 5px;
    background-repeat: no-repeat;
  }

  .graphTypes:focus-visible {
    outline: 2px solid #00a8ff;
    outline-offset: 2px;
  }
</style>
