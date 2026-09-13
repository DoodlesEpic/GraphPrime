<svelte:options runes={true} />

<script lang="ts">
  import { onMount } from "svelte";
  // @ts-expect-error frappe-charts does not ship TypeScript declarations.
  import { Chart as FrappeChartCtor } from "frappe-charts";

  type ChartType = "line" | "bar" | "axis-mixed" | "pie" | "percentage" | "heatmap";

  interface ChartData {
    labels?: (string | number)[];
    datasets?: Array<{
      name?: string;
      values: number[];
      chartType?: ChartType;
    }>;
  }

  interface ChartOptions {
    data: ChartData;
    type?: ChartType;
  }

  interface ChartInstance {
    update(data: ChartData): void;
    destroy?: () => void;
  }

  type ChartConstructor = new (
    parent: string | HTMLElement,
    options: ChartOptions
  ) => ChartInstance;

  const Chart = FrappeChartCtor as unknown as ChartConstructor;

  let { data, type = "line" }: { data: ChartData; type?: ChartType } = $props();

  let chartRoot: HTMLDivElement | undefined;
  let chart: ChartInstance | undefined;

  onMount(() => {
    if (!chartRoot) {
      return;
    }

    chart = new Chart(chartRoot, {
      data,
      type
    });

    return () => {
      chart?.destroy?.();
      chart = undefined;
    };
  });

  $effect(() => {
    if (!chart) {
      return;
    }

    chart.update(data);
  });
</script>

<div class="frappe-chart" bind:this={chartRoot}></div>
