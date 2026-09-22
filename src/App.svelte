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
  let calculationError = $state("");
  let calculationTime = $state(0);
  let compositeNumbers = $state(74);
  let chartType = $state("frappe");
  let algorithm = $state("calculate");

  let chartFullscreen = $state(false);
  let editorFullscreen = $state(false);

  const isCalculateDisabled = $derived(
    calculating || finalValue === undefined || !Number.isSafeInteger(finalValue) || finalValue < 1
  );

  function handleInput(event: Event & { currentTarget: EventTarget & HTMLInputElement }) {
    const newValue = parseInt(event.currentTarget.value.replace(/\D/g, ""));
    finalValue = newValue;
    event.currentTarget.value = newValue.toLocaleString().replace(/NaN/g, "");
  }

  async function calculate() {
    if (isCalculateDisabled || finalValue === undefined) {
      return;
    }

    const chosenFinalValue = finalValue;

    calculating = true;
    calculationError = "";
    const calculationStart = Date.now();

    try {
      primes = await invoke(algorithm, { x: chosenFinalValue });
      chartType = chosenFinalValue >= 10000 ? "dygraph" : "frappe";
      calculationTime = (Date.now() - calculationStart) / 1000;
      lastFinalValue = chosenFinalValue;
      compositeNumbers = chosenFinalValue - primes.length - 1;
    } catch (err) {
      console.error(err);
      calculationError = "Could not calculate prime numbers. Please try again.";
    } finally {
      calculating = false;
    }
  }
</script>

<main>
  <div class="card">
    <h1 class="title">{name}</h1>
    <p>
      Use this application to generate prime sequences and graph them all within the comfort of your
      desktop.
    </p>

    <div class="algorithm-picker">
      <label for="algorithm">Algorithm</label>
      <select id="algorithm" bind:value={algorithm} disabled={calculating}>
        <option value="calculate">Eratosthenes</option>
        <option value="calculate_linear">Linear</option>
      </select>
    </div>

    <div class="input-group">
      <input
        type="text"
        oninput={handleInput}
        class="input"
        min="0"
        max="100000"
        placeholder="100"
        aria-label="Calculate primes up to"
      />
      <button onclick={calculate} disabled={isCalculateDisabled} class="button">Calculate</button>
    </div>
  </div>

  <div class="card" aria-labelledby="algorithm-heading">
    <h2 id="algorithm-heading">
      {algorithm === "calculate" ? "Sieve of Eratosthenes" : "Linear sieve"}
    </h2>
    {#if algorithm === "calculate"}
      <p>
        Marks multiples of each prime to find all primes up to your limit. Its work grows as O(n log
        log n). The optimized implementation is the default for fast calculations.
      </p>
    {:else}
      <p>
        Marks each composite once using its smallest prime factor. Its work grows as O(n), but it
        may use more memory and run slower than the optimized Eratosthenes sieve.
      </p>
    {/if}
    <p>Both algorithms return the same exact primes. Larger limits require more time and memory.</p>
  </div>

  {#if calculationError}
    <p role="alert">{calculationError}</p>
  {/if}

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

  .algorithm-picker {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    margin-bottom: 16px;
  }

  .algorithm-picker select {
    padding: 0.4rem 2rem 0.4rem 0.6rem;
    border: 1px solid var(--border-color);
    border-radius: 5px;
    font: inherit;
    color: var(--body-color);
    background: var(--card-bg);
    appearance: none;
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
