<svelte:options runes={true} />

<script lang="ts">
  import { invoke } from "@tauri-apps/api/core";

  import ProgressBar from "./Components/Cards/ProgressBar.svelte";
  import Stats from "./Components/Cards/Stats.svelte";
  import ScientificGraph from "./Components/Cards/ScientificGraph.svelte";
  import FrappeGraph from "./Components/Cards/FrappeGraph.svelte";
  import Primes from "./Components/Cards/Primes.svelte";

  let { name }: { name: string } = $props();

  let finalValue = $state<number | undefined>();
  let lastFinalValue = $state(100);

  let primes = $state<number[]>([
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97
  ]);

  let calculating = $state(false);
  let calculationTime = $state(0);
  let compositeNumbers = $state(74);
  let chartType = $state("frappe");

  let chartFullscreen = $state(false);
  let editorFullscreen = $state(false);

  const isCalculateDisabled = $derived(
    finalValue === undefined || Number.isNaN(finalValue) || finalValue < 1
  );

  function handleInput(event: Event & { currentTarget: EventTarget & HTMLInputElement }) {
    const newValue = parseInt(event.currentTarget.value.replace(/\D/g, ""));
    finalValue = newValue;
    event.currentTarget.value = newValue.toLocaleString().replace(/NaN/g, "");
  }

  async function calculate() {
    if (finalValue === undefined || Number.isNaN(finalValue) || finalValue < 1) {
      return;
    }

    const chosenFinalValue = finalValue;
    chartType = chosenFinalValue >= 10000 ? "dygraph" : "frappe";

    calculating = true;
    const calculationStart = Date.now();

    try {
      primes = await invoke("calculate", { x: chosenFinalValue });
    } catch (err) {
      console.error(err);
    }

    calculationTime = (Date.now() - calculationStart) / 1000;
    lastFinalValue = chosenFinalValue;
    compositeNumbers = chosenFinalValue - primes.length - 1;
    calculating = false;
  }
</script>

<main>
  <div class="card">
    <h1 class="title">{name}</h1>
    <p>
      Use this application to generate prime sequences and graph them all within the comfort of your
      desktop.
    </p>

    <div class="input-group">
      <input
        type="text"
        oninput={handleInput}
        class="input"
        min="0"
        max="100000"
        placeholder="100"
      />
      <button onclick={calculate} disabled={isCalculateDisabled} class="button">Calculate</button>
    </div>
  </div>

  {#if calculating}
    <ProgressBar />
  {/if}

  {#if primes}
    <Stats {primes} {calculationTime} {compositeNumbers} {lastFinalValue} />

    <Primes bind:editorFullscreen {primes} />

    {#if chartType === "frappe"}
      <FrappeGraph bind:chartType bind:chartFullscreen {primes} />
    {:else}
      <ScientificGraph bind:chartType bind:chartFullscreen {primes} />
    {/if}
  {/if}
</main>

<style>
  :root {
    background: var(--main-bg);
    --graphHeight: 600px;
    --border-color: #ccc;
    --card-bg: white;
    --main-bg: white;
    --body-color: #222;
  }

  /* Dark mode */
  @media (prefers-color-scheme: dark) {
    :root {
      --border-color: #ccc;
      --card-bg: #222;
      --main-bg: #111;
      --body-color: #ffffff;
    }
  }

  main {
    text-align: center;
    padding-bottom: 1em;
    max-width: 1400px;
    margin: 0 auto;
    color: var(--body-color);

    -webkit-user-select: none;
    -ms-user-select: none;
    user-select: none;
    cursor: default;
  }
  .title {
    color: #ff3e00;
    font-size: 3em;
    font-weight: 400;
  }

  .input-group {
    display: flex;
    justify-content: center;
    align-items: stretch;
    gap: 10px;
  }

  .input {
    max-width: 60%;
    flex-grow: 5;
    border: 1px solid var(--border-color);
    border-radius: 5px;
    font-size: 1.2em;
    font-weight: 100;
    font-family: monospace;
    background: var(--card-bg);
    color: var(--body-color);
  }

  .button {
    min-width: 100px;
    max-width: 20%;
    flex-grow: 1;
    border: none;
    border-radius: 5px;
    font-size: 1.2em;
    font-weight: 500;
    background-color: #00a8ff;
    color: white;
  }

  .button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>
