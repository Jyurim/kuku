<script>
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import { is_empty } from "svelte/internal";
  import Swal from "sweetalert2";

  let title = "";
  let content = "";
  let ClassicEditor;
  let ckeditorInstance;

  onMount(async () => {
    const module = await import("@ckeditor/ckeditor5-build-classic");
    ClassicEditor = module.default;
    ClassicEditor.create(document.querySelector("#editor"))
      .then((editor) => {
        ckeditorInstance = editor;
        console.log(editor);
      })
      .catch((error) => {
        console.error(error);
      });
  });

  const postArticle = () =>
    fetch(`//api.eyo.kr:8081/board/qna/answer`, {
      method: "POST",
      headers: {
        Aceept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title,
        content: ckeditorInstance.getData(),
        parentid: $page.params.id,
      }),
      mode: "cors",
      credentials: "include",
    })
      .then((res) => {
        if (res.ok == false) return Promise.reject(res);
        return res.json();
      })
      .then((json) => {
        postResult = JSON.stringify(json);
      })
      .catch((err) => {
        console.log(err);
      });

  const upload = () => {
    console.log(title);
    console.log(
      JSON.stringify({
        title,
        content: ckeditorInstance.getData(),
        parentid: $page.params.id,
      })
    );
    postArticle()
      .then((res) => {
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
        err.text().then((text) => {
          console.log(text);
        });
      });
  };
  const alt = () => {
    Swal.fire({
      title: "제목을 입력해주세요",
      icon: "error",
      confirmButtonText: "확인",
    });
  };
</script>

<!-- 글작성 페이지-->
<form action="POST" on:submit|preventDefault={upload}>
  <div class="content">
    <div class="write__title" style="text-align: left; font-size: 30px;" />
    <form>
      <div class="write__form__title" style="margin-top: 2px;">
        <h1>A</h1>
        <input
          class="input mb-4"
          id="title"
          placeholder="제목을 입력해주세요."
          bind:value={title}
          required
        />
        <div class="write__form__content">
          <textarea
            class="textarea"
            id="editor"
            placeholder="답변을 입력해주세요."
            required>{content}</textarea
          >
        </div>
      </div>
    </form>
  </div>
</form>

<br /><br /><br />

{#if is_empty(title)}
  <button class="button is-success" on:click={alt}>작성</button>
{:else}
  <a href="/board/qna/article/{$page.params.id}">
    <button class="button is-success" type="submit" on:click={upload}>
      작성
    </button>
  </a>
{/if}
<a href="/board/qna/article/{$page.params.id}">
  <button class="button is-danger">취소</button>
</a>

<br /><br />

<style>
  :global(.ck-editor__editable_inline) {
    min-height: 400px;
  }
</style>
