<script>
	onMount(() => {
		if (browser)
			window.onbeforeunload = function () {
				return true;
			};
	});
	onDestroy(() => {
		if (browser) window.onbeforeunload = null;
	});

	import { onMount } from "svelte";
	import { browser } from "$app/env";
	import { page } from "$app/stores";
	import { is_empty, onDestroy } from "svelte/internal";
	import Swal from "sweetalert2";
	import CodeEditor from "$lib/codeEditor.svelte";

	let title = "",
		content = "",
		code = "",
		chapter_id = $page.params.id.match(/\d+/);

	let courses = [];
	let chapters = [{ id: "", no: null, title: "(최상위)" }];
	let language = [
		{
			name: "Cpp",
			code: '#include <stdio.h>\n\nint main() {\n\tint a = 0;\n\tscanf("%d", &a);\n\tprintf("%d", a);\n\n\treturn 0;\n}',
		},
		{
			name: "Python",
			code: "a = int(input())\nprint(a)",
		},
		{
			name: "Java",
			code: "import java.util.Scanner;\n\npublic class Main {\n\tpublic static void main(String[] args) {\n\t\tScanner sc = new Scanner(System.in);\n\t\tint a = sc.nextInt();\n\t\tSystem.out.println(a);\n\t}\n}",
		},
	];
	let categories = [];

	let articles = [];

	let selected_course = "";
	let parent_chapter = "null";
	let selected_language = language[0].name;
	let category = "";

	let getCodeData;

	if (browser) {
		fetch("//api.eyo.kr:8081/study/courses", {
			method: "GET",
			headers: {
				Accept: "application/json",
			},
			mode: "cors",
			credentials: "include",
		})
			.then((resp) => resp.json())
			.then((data) => {
				courses = data;
			});

		fetch("//api.eyo.kr:8081/study/categories", {
			method: "GET",
			headers: {
				Accept: "application/json",
			},
			mode: "cors",
			credentials: "include",
		})
			.then((resp) => resp.json())
			.then((data) => {
				categories = data.map((item) => item.category);
			});

		if (chapter_id != undefined) {
			fetch("//api.eyo.kr:8081/study/chapter/" + chapter_id, {
				method: "GET",
				headers: {
					Accept: "application/json",
				},
				mode: "cors",
				credentials: "include",
			})
				.then((resp) => resp.json())
				.then((data) => {
					selected_course = data.course_slug;
					parent_chapter = data.parent_id ?? "null";
					category = data.category;
					title = data.title;
					content = data.content;

					update_courses(selected_course)
						.then(function (r) {
							select_title(title);
						})
						.catch((err) => console.log(err));
				});
		}
	}

	$: update_courses(selected_course);
	async function update_courses(selected_course) {
		if (browser && selected_course != undefined && selected_course != "") {
			return fetch(`//api.eyo.kr:8081/study/${selected_course}/list`, {
				method: "GET",
				headers: {
					Accept: "application/json",
				},
				mode: "cors",
				credentials: "include",
			})
				.then((resp) => resp.json())
				.then((data) => {
					chapters = [
						{ id: "", title: "(최상위)", parent: null, no: null },
					];
					function traverse(current, parent_id) {
						let node = Object.assign({}, current);

						node["parent"] = parent_id;
						chapters.push(node);

						current.children.forEach((child) => {
							traverse(child, current.course_id);
						});
					}
					data.forEach((data) => traverse(data, ""));

					return Promise.resolve();
				});
		}

		return Promise.resolve();
	}

	$: select_title(title);
	function select_title(selected_title) {
		if (browser && selected_title != "") {
			const chapter = chapters.find(
				(item) => item.title == selected_title
			);

			if (chapter == undefined) return;
			if (chapter_id != chapter.no) {
				window.location.href = `/study/write/${chapter.no}`;
				return;
			}

			chapter_id = chapter.no;
			title = chapter.title;
			content = chapter.content;
			parent_chapter = chapter.parent_id ?? "null";
			category = chapter.category;

			fetch(`//api.eyo.kr:8081/study/${selected_course}/${chapter_id}/`, {
				method: "GET",
				headers: {
					Accept: "application/json",
				},
				mode: "cors",
				credentials: "include",
			})
				.then((resp) => resp.json())
				.then((data) => {
					articles = data;

					load_article_of_language(selected_language, articles);
				});
		}
	}

	$: load_article_of_language(selected_language, articles);
	function load_article_of_language(language, articles) {
		if (browser && language != undefined && articles != undefined) {
			const article = articles.find((item) => item.language == language);

			if (article == undefined) return;

			content = article.content;
			ckeditorInstance.setData(content);

			code = article.code;
		}
	}

	let ckeditorInstance;
	// let ClassicEditor;
	onMount(async () => {
		if (browser)
			ClassicEditor.create(document.querySelector("#editor"), {
				simpleUpload: {
					// The URL that the images are uploaded to.
					uploadUrl: "//api.eyo.kr:8081/upload/",

					// Enable the XMLHttpRequest.withCredentials property.
					withCredentials: true,
				},
			})
				.then((editor) => {
					ckeditorInstance = editor;
				})
				.catch((error) => {
					console.error(error);
				});
	});

	const postArticle = async () => {
		if (title == "") {
			alert("제목을 입력해주세요.");
			return;
		}

		let data = {
			title: title,
			language: selected_language,
			parent_id: parent_chapter == "null" ? null : parent_chapter,
			category: category,
			chapter_id: chapter_id,

			content: ckeditorInstance.getData(),
			code: getCodeData(),
		};

		fetch(`//api.eyo.kr:8081/study/${selected_course}/`, {
			method: "POST",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
			},
			mode: "cors",
			credentials: "include",
			body: JSON.stringify(data),
		}).then(function (resp) {
			if (resp.ok) {
				alert("등록되었습니다.");
				window.location.href = `/study/write/`;
			}
		});
	};
</script>

<svelte:head>
	<script src="/ckeditor.js"></script>
</svelte:head>

<br />
<div class="editor">
	<form method="POST" on:submit|preventDefault={postArticle}>
		<div class="contents">
			<header class="control">
				<div class="columns m-0">
					<div class="is-one-fifth select">
						<select bind:value={selected_course}>
							<option value="" disabled selected>강의</option>
							{#each courses as c}
								<option value={c.slug}>{c.title}</option>
							{/each}
						</select>
					</div>
					<div class="is-one-fifth select">
						<select bind:value={parent_chapter}>
							<option value="null" disabled selected
								>상위 카테고리</option
							>
							{#each chapters as c}
								<option value={c.no}>{c.title}</option>
							{/each}
						</select>
					</div>
					<div class="is-one-fifth select">
						<select bind:value={selected_language}>
							<option value="" disabled selected>언어</option>
							{#each language as lang}
								<option value={lang.name}>{lang.name}</option>
							{/each}
						</select>
					</div>
					<div class="is-one-fifth">
						<input
							class="input"
							type="text"
							placeholder="주요 카테고리명"
							list="categories"
							bind:value={category}
						/>
						<datalist id="categories">
							{#each categories as c}
								<option value={c} />
							{/each}
						</datalist>
					</div>
				</div>
				<div class="mt-2">
					<input
						class="mb-4 input"
						type="text"
						placeholder="챕터 명을 입력해주세요"
						bind:value={title}
						list="chapters"
						required
					/>
					<datalist id="chapters">
						{#each chapters.filter((e) => e.id != "") as c}
							<option value={c.title} />
						{/each}
					</datalist>
				</div>
			</header>
			<textarea
				class="textarea"
				id="editor"
				placeholder="내용을 입력하세요.">{content}</textarea
			>
			<hr />
			<h2 class="title">기본 예제코드</h2>
			<CodeEditor
				language={selected_language}
				code={code != ""
					? code
					: language.find((lang) => lang.name == selected_language)
							.code}
				bind:getData={getCodeData}
			/>
			<br /><br /><br />
		</div>
		<button class="button is-link">완료</button>
	</form>
</div>
<br /> <br />

<style>
	header.control select {
		margin-right: 4px;
		width: 155px;
	}
	.editor {
		width: calc(100% - 400px - 8px);
		margin: 0 auto;
	}
	textarea {
		width: 100%;
		height: 80em;
		resize: none;
	}

	CodeEditor {
		height: 80em;
	}

	:global(.ck-editor__editable_inline) {
		min-height: 600px;
	}
</style>
