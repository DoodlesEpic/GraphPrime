<script lang="ts">
  import { slide } from "svelte/transition";
</script>

<div class="bar" in:slide out:slide />

<style>
  @keyframes moving-gradient {
    0% {
      background-position: left bottom;
    }
    100% {
      background-position: right bottom;
    }
  }

  .bar {
    margin: 1em;
    padding: 1em;
    border-radius: 5px;

    background: -webkit-linear-gradient(
        left,
        #00a5e6 30%,
        #a2e8f3 60%,
        #00a5e6 100%
      )
      repeat;

    animation-duration: 2s;
    background-size: 50% 100%;
    animation-name: moving-gradient;
    animation-duration: 1s;
    animation-iteration-count: infinite;
    animation-timing-function: linear;
  }
</style>
