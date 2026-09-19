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
    <button aria-label="Copy primes" onclick={() => writeText(primes.join(", "))}
      ><Fa icon={faClipboard} fw /></button
    >
    <button
      aria-label="Toggle primes fullscreen"
      onclick={() => (editorFullscreen = !editorFullscreen)}><Fa icon={faExpand} fw /></button
    >
  </div>
  <h2>Primes</h2>
  <div class="prime-list">
    <CodeMirror {primes} {editorFullscreen} />
  </div>
</div>

<style>
  #primes {
    overflow: hidden;
  }

  .prime-list {
    font-size: 1.1em;
    font-weight: 100;
    font-family: monospace;
    font-variant-numeric: tabular-nums;
  }
</style>
