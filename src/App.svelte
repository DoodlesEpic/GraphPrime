<script lang="ts">
  // Svelte and Tauri
  import { invoke } from "@tauri-apps/api/tauri";

  // Components
  import ProgressBar from "./Components/Cards/ProgressBar.svelte";
  import Stats from "./Components/Cards/Stats.svelte";
  import ScientificGraph from "./Components/Cards/ScientificGraph.svelte";
  import FrappeGraph from "./Components/Cards/FrappeGraph.svelte";
  import Primes from "./Components/Cards/Primes.svelte";
  export let name: string;

  // Primes will be calculated upto this number
  let finalValue: number;
  let lastFinalValue = 100;

  // Hardcoded data upto 100 for initializing the chart
  let primes: number[] = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97,
  ];

  let calculating = false;
  let calculationTime = 0;
  let compositeNumbers = 74; // Hardcoded value for the default prime numbers
  let chartType = "frappe";

  // Track which cards are fullscreen
  let chartFullscreen = false;
  let editorFullscreen = false;

  function handleInput(event: any) {
    // The new value, but remove all characters and keep only the digits
    const newValue = parseInt(event.target.value.replace(/\D/g, ""));

    // Update the value to calculate to the new number
    finalValue = newValue;

    // Show the new value with the thousand separator applied
    event.target.value = newValue.toLocaleString().replace(/NaN/g, "");
    console.log(finalValue);
  }

  async function calculate() {
    // Save because finalValue binds to input and may change during calculation
    const chosenFinalValue = finalValue;

    // Change chart to dygraph if we have too much data to prevent crashes
    if (chosenFinalValue >= 10000) chartType = "dygraph";
    else chartType = "frappe";

    // Start the timer
    calculating = true;
    const calculationStart = Date.now();

    // Calculate primes upto finalValue
    try {
      primes = await invoke("calculate", { x: chosenFinalValue });
    } catch (err) {
      console.error(err);
    }

    // Update stats
    calculationTime = (Date.now() - calculationStart) / 1000;
    lastFinalValue = chosenFinalValue;
    compositeNumbers = chosenFinalValue - primes.length - 1; // -1 because 2 doesn't count as a composite number
    calculating = false;
  }
</script>

<main>
  <div class="card">
    <h1 class="title">{name}</h1>
    <p>
      Use this application to generate prime sequences and graph them all within
      the comfort of your desktop.
    </p>

    <div class="input-group">
      <input
        type="text"
        on:input={handleInput}
        class="input"
        min="0"
        max="100000"
        placeholder="100"
      />
      <button
        on:click={calculate}
        disabled={finalValue < 1 ||
          finalValue === undefined ||
          Number.isNaN(finalValue)}
        class="button">Calculate</button
      >
    </div>
  </div>

  {#if calculating}
    <ProgressBar />
  {/if}

  {#if primes}
    <Stats {primes} {calculationTime} {compositeNumbers} {lastFinalValue} />

    <Primes {editorFullscreen} {primes} />

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

    /* Prevent text selection to make the application feel more native */
    /* The prime number list can still be copied because it's under CodeMirror's textarea */
    -webkit-user-select: none; /* Safari */
    -ms-user-select: none; /* Edge */
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
