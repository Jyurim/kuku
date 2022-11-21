<script>
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import Swal from "sweetalert2";
  let answer_data = { title: "", content: "" };
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

  const getanswer = async (article_id) => {
    const res = await fetch(
      `//api.eyo.kr:8081/board/qna/list/article/${article_id}`,
      {
        mode: "cors",
        credentials: "include",
      }
    );
    const article = await res.json();
    answer_data = article;
    if (ckeditorInstance != undefined)
      ckeditorInstance.setData(answer_data.content);

    if (res.ok) {
      return article;
    } else {
      throw new Error(article);
    }
  };
  let article = getanswer($page.params.ansid);

  const putanswer = async (answer_id) => {
    const res = await fetch(`//api.eyo.kr:8081/board/qna/answer/${answer_id}`, {
      method: "PUT",
      headers: {
        Aceept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: answer_data.title,
        content: ckeditorInstance.getData(),
      }),
      mode: "cors",
      credentials: "include",
    })
      .then((res) => {
        if (res.ok == false) return Promise.reject(res);
        return res.json();
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const upload = () => {
    console.log(
      JSON.stringify({
        title: answer_data.title,
        content: ckeditorInstance.getData(),
      })
    );
    Swal.fire({
      title: "수정하시겠습니까?",
      text: "",
      icon: "question",
      showCancelButton: true,
      confirmButtonColor: "rgb(067, 085, 189)",
      cancelButtonColor: "rgb(219, 224, 255)",
      confirmButtonText: "수정",
      cancelButtonText: "취소",
      preConfirm: () => {
        putanswer($page.params.ansid)
          .then((res) => {
            console.log(res);
          })
          .catch((err) => {
            console.log(err);
            err.text().then((text) => {
              console.log(text);
            });
          });
      },
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire("Motified!", "글이 수정되었습니다.", "success").then(
          (result) => {
            if (result.isConfirmed)
              location.href = "/board/qna/article/" + $page.params.id;
          }
        );
      }
    });
  };
</script>

<!-- 글작성 페이지-->
<form method="PUT" on:submit|preventDefault={upload}>
  <div class="contents">
    <div class="write__title" style="text-align: left; font-size: 30px;" />
    <form>
      <div class="write__form__title" style="margin-top: 2px;">
        <h1>A</h1>
        <input
          class="input mb-4"
          id="title"
          placeholder="제목을 입력해주세요."
          bind:value={answer_data.title}
          required
        />
        <div class="write__form__content">
          <textarea
            class="textarea"
            id="editor"
            placeholder="답변을 입력해주세요."
            required>{answer_data.content}</textarea
          >
        </div>
      </div>
    </form>
  </div>
</form>

<br /><br /><br />

<div class="buttons">
  <button class="button is-success" type="submit" on:click={upload}>
    작성
  </button>
  <a href="/board/qna/article/{$page.params.id}">
    <button class="button is-danger">취소</button>
  </a>
</div>

<br /><br />

<style>
  :global(.ck-editor__editable_inline) {
    min-height: 400px;
  }
</style>
