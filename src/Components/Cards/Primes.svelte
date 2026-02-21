<svelte:options runes={true} />

<script lang="ts">
  import { writeText } from "@tauri-apps/plugin-clipboard-manager";
  import CodeMirror from "../Util/CodeMirror.svelte";
  import Fa from "svelte-fa";
  import { faExpand, faClipboard } from "@fortawesome/free-solid-svg-icons";

  let {
    editorFullscreen = $bindable(),
    primes
  }: {
    editorFullscreen: boolean;
    primes: number[];
  } = $props();
</script>

<div id="primes" class="card" class:fullscreen={editorFullscreen}>
  <div class="copyfullButtons">
    <button onclick={() => writeText(primes.join(", "))}><Fa icon={faClipboard} fw /></button>
    <button onclick={() => (editorFullscreen = !editorFullscreen)}><Fa icon={faExpand} fw /></button
    >
  </div>
  <h2>Primes</h2>
  <p>
    <CodeMirror bind:primes bind:editorFullscreen />
  </p>
</div>

<style>
  #primes {
    overflow: hidden;
  }

  #primes p {
    font-size: 1.1em;
    font-weight: 100;
    font-family: monospace;
    font-variant-numeric: tabular-nums;
  }
</style>
