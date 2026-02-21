<svelte:options runes={true} />

<script lang="ts">
  let {
    primes,
    calculationTime,
    compositeNumbers,
    lastFinalValue
  }: {
    primes: number[];
    calculationTime: number;
    compositeNumbers: number;
    lastFinalValue: number;
  } = $props();
</script>

<div class="card">
  <h2>Stats</h2>
  <p>
    {primes.length} prime numbers calculated up to {lastFinalValue}
  </p>
  <p>The calculation took {calculationTime} seconds</p>
  <p>
    There are {compositeNumbers} composite numbers up to {lastFinalValue}
  </p>
</div>
