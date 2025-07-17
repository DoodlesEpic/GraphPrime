<script lang="ts">
  import { writeText } from "@tauri-apps/plugin-clipboard-manager";
  import CodeMirror from "../Util/CodeMirror.svelte";
  import Fa from "svelte-fa";
  import { faExpand, faClipboard } from "@fortawesome/free-solid-svg-icons";

  export let editorFullscreen: boolean;
  export let primes: number[];
</script>

<div id="primes" class={"card"} class:fullscreen={editorFullscreen}>
  <div class="copyfullButtons">
    <button on:click={() => writeText(primes.join(", "))}><Fa icon={faClipboard} fw /></button>
    <button on:click={() => (editorFullscreen = !editorFullscreen)}
      ><Fa icon={faExpand} fw /></button
    >
  </div>
  <h2>Primes</h2>
  <p>
    <CodeMirror bind:primes bind:editorFullscreen />
  </p>
</div>

<style>
  #primes {
    /* Use the codemirror scroll for performance */
    overflow: hidden;
  }

  #primes p {
    /* Comfortable font for reading huge amounts of data */
    font-size: 1.1em;
    font-weight: 100;
    font-family: monospace;
    font-variant-numeric: tabular-nums;
  }
</style>
