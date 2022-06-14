<!-- 
    Adapted from https://svelte.dev/repl/a199ca2d451e4b0b92a8abd2d0e71ec6?version=3.35.0
    As an alternative to @joshnuss/svelte-codemirror
    Removed a lot of unnecessary code from the original example, specifically the styling
 -->
<script lang="ts">
  import { onMount } from "svelte";
  import CodeMirror from "codemirror";

  export let options = {};
  export let editor: CodeMirror.Editor;

  let element: HTMLElement;

  onMount(() => {
    createEditor(options);
  });

  $: if (element) {
    createEditor(options);
  }

  function createEditor(options: CodeMirror.EditorConfiguration) {
    if (editor) element.innerHTML = "";
    editor = CodeMirror(element, options);
  }
</script>

<div bind:this={element} />

<style>
  :root {
    --maximumHeight: 400px;
  }

  @media (prefers-color-scheme: light) {
    :root {
      --cm-border-color: #ccc;
      --cm-background-color: white;
      --cm-medium-color: #ccc;
      --cm-text-color: #222;
    }
  }

  @media (prefers-color-scheme: dark) {
    :root {
      --cm-border-color: #ccc;
      --cm-background-color: #222;
      --cm-medium-color: #ccc;
      --cm-text-color: white;
    }
  }

  /* BASICS */
  :global(.cm) {
    /* Set height, width, borders, and global font properties here */
    font-family: monospace;
    height: auto;
    direction: ltr;
    color: var(--cm-text-color);
    background: var(--cm-background-color);
  }

  /* CURSOR */

  :global(.cm-cursor) {
    border-left: 2px solid var(--cm-medium-color);
    border-right: none;
    width: 0;
  }
  /* Shown when moving in bi-directional text */
  :global(.cm div.cm-secondarycursor) {
    border-left: 1px solid var(--cm-medium-color);
  }
  :global(.cm-fat-cursor .cm-cursor) {
    width: auto;
    border: 0 !important;
    background: var(--cursor-color);
  }
  :global(.cm-fat-cursor div.cm-cursors) {
    z-index: 1;
  }
  :global(.cm-fat-cursor-mark) {
    background-color: var(--cursor-color);
    -webkit-animation: blink 1.06s steps(1) infinite;
    -moz-animation: blink 1.06s steps(1) infinite;
    animation: blink 1.06s steps(1) infinite;
  }
  :global(.cm-animate-fat-cursor) {
    width: auto;
    border: 0;
    -webkit-animation: blink 1.06s steps(1) infinite;
    -moz-animation: blink 1.06s steps(1) infinite;
    animation: blink 1.06s steps(1) infinite;
    background-color: var(--cursor-color);
  }
  @-moz-keyframes blink {
    0% {
    }
    50% {
      background-color: transparent;
    }
    100% {
    }
  }
  @-webkit-keyframes blink {
    0% {
    }
    50% {
      background-color: transparent;
    }
    100% {
    }
  }
  @keyframes blink {
    0% {
    }
    50% {
      background-color: transparent;
    }
    100% {
    }
  }

  :global(.cm-tab) {
    display: inline-block;
    text-decoration: inherit;
  }

  /* Default styles for common addons */

  :global(div.cm span.cm-matchingbracket) {
    color: #0b0;
  }
  :global(div.cm span.cm-nonmatchingbracket) {
    color: #a22;
  }
  :global(.cm-matchingtag) {
    background: rgba(255, 150, 0, 0.3);
  }
  :global(.cm-activeline-background) {
    background: #e8f2ff;
  }

  /* STOP */

  /* The rest of this file contains styles related to the mechanics of
     the editor. You probably shouldn't touch them. */

  :global(.cm) {
    position: relative;
    overflow: hidden;
  }

  :global(.cm-scroll) {
    overflow: scroll !important; /* Things will break if this is overridden */
    /* 30px is the magic margin used to hide the element's real scrollbars */
    /* See overflow: hidden in .cm */
    margin-bottom: -30px;
    margin-right: -30px;
    padding-bottom: 30px;
    height: 100%;
    outline: none; /* Prevent dragging from highlighting the element */
    position: relative;

    min-height: 40px;
    max-height: var(--maximumHeight);
  }
  :global(.cm-sizer) {
    position: relative;
    border-right: 30px solid transparent;
  }

  /* The fake, visible scrollbars. Used to force redraw during scrolling
     before actual scrolling happens, thus preventing shaking and
     flickering artifacts. */
  :global(.cm-vscrollbar, .cm-hscrollbar, .cm-scrollbar-filler, .cm-gutter-filler) {
    position: absolute;
    z-index: 6;
    display: none;
  }

  :global(.cm ::-webkit-scrollbar) {
    width: 8px;
    height: 8px;
  }

  :global(.cm ::-webkit-scrollbar-track) {
    background: #f4f4f4;
    border-radius: 10px;
  }

  :global(.cm ::-webkit-scrollbar-thumb) {
    border-radius: 10px;
    background: var(--cm-medium-color);
  }

  :global(.cm-vscrollbar) {
    right: 0;
    top: 0;
    overflow-x: hidden;
    overflow-y: scroll;
  }
  :global(.cm-hscrollbar) {
    bottom: 0;
    left: 0;
    overflow-y: hidden;
    overflow-x: scroll;
    height: 8px;
  }
  :global(.cm-scrollbar-filler) {
    right: 0;
    bottom: 0;
  }
  :global(.cm-gutter-filler) {
    left: 0;
    bottom: 0;
  }

  :global(.cm-gutters) {
    position: absolute;
    left: 0;
    top: 0;
    min-height: 100%;
    z-index: 3;
  }
  :global(.cm-gutter) {
    white-space: normal;
    height: 100%;
    display: inline-block;
    vertical-align: top;
    margin-bottom: -30px;
  }
  :global(.cm-gutter-wrapper) {
    position: absolute;
    z-index: 4;
    background: none !important;
    border: none !important;
  }
  :global(.cm-gutter-background) {
    position: absolute;
    top: 0;
    bottom: 0;
    z-index: 4;
  }
  :global(.cm-gutter-elt) {
    position: absolute;
    cursor: default;
    z-index: 4;
  }
  :global(.cm-gutter-wrapper ::selection) {
    background-color: transparent;
  }
  :global(.cm-gutter-wrapper ::-moz-selection) {
    background-color: transparent;
  }

  :global(.cm-lines) {
    cursor: text;
    min-height: 1px; /* prevents collapsing before first draw */
  }
  :global(.cm pre.cm-line, .cm pre.cm-line-like) {
    /* Reset some styles that the rest of the page might have set */
    -moz-border-radius: 0;
    -webkit-border-radius: 0;
    border-radius: 0;
    border-width: 0;
    background: transparent;
    font-family: inherit;
    font-size: inherit;
    margin: 0;
    white-space: pre;
    word-wrap: normal;
    line-height: inherit;
    color: inherit;
    z-index: 2;
    position: relative;
    overflow: visible;
    -webkit-tap-highlight-color: transparent;
    -webkit-font-variant-ligatures: contextual;
    font-variant-ligatures: contextual;
  }
  :global(.cm-wrap pre.cm-line, .cm-wrap pre.cm-line-like) {
    word-wrap: break-word;
    white-space: pre-wrap;
    word-break: normal;
  }

  :global(.cm-linebackground) {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    z-index: 0;
  }

  :global(.cm-linewidget) {
    position: relative;
    z-index: 2;
    padding: 0.1px; /* Force widget margins to stay inside of the container */
  }

  :global(.cm-rtl pre) {
    direction: rtl;
  }

  :global(.cm-code) {
    outline: none;
  }

  /* Force content-box sizing for the elements where we expect it */
  :global(.cm-scroll, .cm-sizer, .cm-gutter, .cm-gutters, .cm-linenumber) {
    -moz-box-sizing: content-box;
    box-sizing: content-box;
  }

  :global(.cm-measure) {
    position: absolute;
    width: 100%;
    height: 0;
    overflow: hidden;
    visibility: hidden;
  }

  :global(.cm-cursor) {
    position: absolute;
    pointer-events: none;
  }
  :global(.cm-measure pre) {
    position: static;
  }

  :global(div.cm-cursors) {
    /* always show cursor */
    visibility: visible;
    position: relative;
    z-index: 3;
  }
  :global(div.cm-dragcursors) {
    visibility: visible;
  }

  :global(.cm-focused div.cm-cursors) {
    visibility: visible;
  }

  :global(.cm-selected) {
    background: #d9d9d9;
  }
  :global(.cm-focused .cm-selected) {
    background: #d7d4f0;
  }
  :global(.cm-crosshair) {
    cursor: crosshair;
  }
  :global(.cm-line::selection, .cm-line > span::selection, .cm-line
      > span
      > span::selection) {
    background: #d7d4f0;
  }
  :global(.cm-line::-moz-selection, .cm-line > span::-moz-selection, .cm-line
      > span
      > span::-moz-selection) {
    background: #d7d4f0;
  }

  :global(.cm-searching) {
    background-color: #ffa;
    background-color: rgba(255, 255, 0, 0.4);
  }

  /* Used to force a border model for a node */
  :global(.cm-force-border) {
    padding-right: 0.1px;
  }

  @media print {
    /* Hide the cursor when printing */
    :global(.cm div.cm-cursors) {
      visibility: hidden;
    }
  }

  /* See issue #2901 */
  :global(.cm-tab-wrap-hack:after) {
    content: "";
  }

  /* Help users use markselection to safely style text background */
  :global(span.cm-selectedtext) {
    background: none;
  }
</style>
