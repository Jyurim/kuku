<script>
	export let language;
	export let code;
	export let getData;

	import { onMount } from "svelte";
	import { browser } from "$app/env";
	import editorWorker from "monaco-editor/esm/vs/editor/editor.worker?worker";
	import jsonWorker from "monaco-editor/esm/vs/language/json/json.worker?worker";
	import cssWorker from "monaco-editor/esm/vs/language/css/css.worker?worker";
	import htmlWorker from "monaco-editor/esm/vs/language/html/html.worker?worker";
	import tsWorker from "monaco-editor/esm/vs/language/typescript/ts.worker?worker";

	let divEl = null;
	let editor;
	let Monaco;

	$: {
		if (browser && editor != undefined) {
			Monaco.editor.setModelLanguage(
				editor.getModel(),
				language.toLocaleLowerCase()
			);
		}
	}
	$: {
		if (browser && editor != undefined) {
			editor.getModel().setValue(code);
		}
	}
	getData = () => {
		return editor.getModel().getValue();
	};

	onMount(async () => {
		// @ts-ignore
		self.MonacoEnvironment = {
			getWorker: function (_moduleId, label) {
				if (label === "json") {
					return new jsonWorker();
				}
				if (label === "css" || label === "scss" || label === "less") {
					return new cssWorker();
				}
				if (
					label === "html" ||
					label === "handlebars" ||
					label === "razor"
				) {
					return new htmlWorker();
				}
				if (label === "typescript" || label === "javascript") {
					return new tsWorker();
				}
				return new editorWorker();
			},
		};

		Monaco = await import("monaco-editor");
		editor = Monaco.editor.create(divEl, {
			theme: "vs-dark",
			value: code,
			language: language.toLocaleLowerCase(),
		});

		return () => {
			editor.dispose();
		};
	});
</script>

<div bind:this={divEl} class="h-screen" />

<style>
	.h-screen {
		height: calc(100vh - 252px);
	}
</style>
