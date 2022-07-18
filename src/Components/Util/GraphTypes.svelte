<script lang="ts">
  export let chartType: string;
</script>

<select name="Graph Types" class="graphTypes" bind:value={chartType}>
  <option value="frappe">Basic</option>
  <option value="dygraph">Scientific</option>
</select>

<style>
  .graphTypes {
    position: absolute;
    left: 10px;
    /* No dark mode is applied because of webkitgtk */
    /* See https://github.com/DoodlesEpic/GraphPrime/issues/37 */
  }
</style>
