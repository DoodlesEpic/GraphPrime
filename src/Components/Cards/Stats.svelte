<script lang="ts">
  export let primes: number[];
  export let calculationTime: number;
  export let compositeNumbers: number;
  export let lastFinalValue: number;
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
