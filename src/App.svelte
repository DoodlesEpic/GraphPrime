<script lang="ts">
  export let name: string;
  let finalValue: number;
  let primes: number[] = [];

  function isPrime(x) {
    for (let i = 2; i < x; i++) {
      if (x % i == 0) {
        return false;
      }
    }
    return true;
  }

  function calculate() {
    primes = [];
    for (let i = 2; i < finalValue; i++) {
      if (isPrime(i)) {
        primes.push(i);
      }
    }
    primes = primes; // Force Svelte to trigger an update
  }
</script>

<main>
  <h1>Welcome to {name}!</h1>
  <p>
    Use this application to generate prime sequences and graph them all within
    the comfort of your desktop.
  </p>

  <input type="number" bind:value={finalValue} min="0" max="100000" />
  <button on:click={calculate}>Calculate</button>

  {#if finalValue}
    <p>{finalValue}</p>
  {/if}

  {#if primes}
    <p>
      {primes.join(", ")}
    </p>
  {/if}
</main>

<style>
  main {
    text-align: center;
    padding: 1em;
    max-width: 240px;
    margin: 0 auto;
  }

  h1 {
    color: #ff3e00;
    font-size: 4em;
    font-weight: 100;
  }

  @media (min-width: 640px) {
    main {
      max-width: none;
    }
  }
</style>
