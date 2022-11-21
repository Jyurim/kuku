<script>
  import { page } from "$app/stores";
  import List from "../../[page]/+page.svelte";
  import Swal from "sweetalert2";
  import { onMount } from "svelte";

  const getArticle = async (article_id) => {
    const res = await fetch(
      `//api.eyo.kr:8081/board/free/article_id/${article_id}`,
      {
        mode: "cors",
        credentials: "include",
      }
    );
    const article = await res.json();
    if (res.ok) {
      return article;
    } else {
      throw new Error(article);
    }
  };
  $: article = getArticle($page.params.id);

  const delArticle = async (article_id) => {
    const res = await fetch(
      `//api.eyo.kr:8081/board/free/delete/${article_id}`,
      {
        method: "DELETE",
        mode: "cors",
        credentials: "include",
      }
    );
    const article = await res.json();
    if (res.ok) {
      return article;
    } else {
      throw new Error(article);
    }
  };
  const del = () => {
    Swal.fire({
      title: "삭제하시겠습니까?",
      text: "다시 되돌릴 수 없습니다.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "rgb(067, 085, 189)",
      cancelButtonColor: "rgb(219, 224, 255)",
      confirmButtonText: "삭제",
      cancelButtonText: "취소",
      preConfirm: () => {
        delArticle($page.params.id)
          .then((res) => {
            console.log(res);
          })
          .catch((err) => {
            console.log(err);
            Swal.fire({
              title: "본인이 작성한 글만 삭제\n할 수 있습니다.",
              text: "",
              icon: "error",
              confirmButtonColor: "rgb(067, 085, 189)",
            });
            err.text().then((text) => {
              // console.log(text);
            });
          });
      },
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire("Deleted!", "글이 삭제되었습니다.", "success").then(
          (result) => {
            if (result.isConfirmed) location.href = "/board/free/1";
          }
        );
      }
    });
  };
  const getComment = async (article_id) => {
    const res = await fetch(
      `//api.eyo.kr:8081/board/free/comment/${article_id}`,
      {
        mode: "cors",
        credentials: "include",
      }
    );
    const comment = await res.json();
    if (res.ok) {
      return comment;
    } else {
      throw new Error(comment);
    }
  };
  $: comments = getComment($page.params.id);

  const Like = async (article_id) => {
    const res = await fetch(
      `//api.eyo.kr:8081/board/free/article/${article_id}/like`,
      {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        mode: "cors",
        credentials: "include",
      }
    );
    const json = await res.json();
    postLikeResult = JSON.stringify(json);
  };

  const disLike = async (article_id) => {
    const res = await fetch(
      `//api.eyo.kr:8081/board/free/article/${article_id}/dislike`,
      {
        method: "PUT",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        mode: "cors",
        credentials: "include",
      }
    );
    const json = await res.json();
    disLikeResult = JSON.stringify(json);
  };

  let isClicked = false;
  const likeclick = () => {
    isClicked = !isClicked;
  };
  const alt = () => {
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: "로그인이 필요합니다!",
      footer: "",
    });
  };
  let isLogin = true;
  let comment_content = "";
  const create_comment = async (article_id) => {
    return await fetch(
      `//api.eyo.kr:8081/board/free/comment/create/${article_id}`,
      {
        method: "POST",
        headers: {
          Aceept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          content: comment_content,
        }),
        mode: "cors",
        credentials: "include",
      }
    );
  };
  const upload = () => {
    create_comment($page.params.id)
      .then((res) => {
        console.log(res);
        if (res.ok == false) {
          return Promise.reject(res);
        } else {
          return res.json();
        }
      })
      .then(
        Swal.fire("Good job!", "댓글이 생성되었습니다!", "success").then(
          function (isConfirm) {
            location.reload(isConfirm);
          }
        )
      )
      .catch((err) => {
        console.error(err);
      });
  };
  const delete_comment = async (comment_id) => {
    await fetch(`//api.eyo.kr:8081/board/free/comment/delete/${comment_id}`, {
      method: "PUT",
      headers: {
        Aceept: "application/json",
      },
      mode: "cors",
      credentials: "include",
    })
      .then((res) => {
        console.log(res);
        if (res.ok == false) {
          return Promise.reject(res);
        } else {
          return res.json();
        }
      })
      .then(
        Swal.fire("Good job!", "댓글이 삭제되었습니다!", "success").then(
          function (isConfirm) {
            location.reload(isConfirm);
          }
        )
      )
      .catch((err) => {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "본인의 글만 삭제할 수 있습니다!",
        });
      });
  };
  onMount(async () => {
    if (window.sessionStorage["user.username"] == null) {
      isLogin = false;
    }
  });
</script>

{#await article}
  <p class="has-text-centered">Loading in progress...</p>
{:then article}
  <header>
    <div style="padding: 16px">
      {#if isLogin}
        {#if Number(window.sessionStorage["user.id"]) == article.userid}
          <div class="edit" style="float: right; margin-top: 16px">
            <a href="/board/free/write/{article.article_id}">
              <button class="button is-rounded is-light"> 수정 </button>
            </a>
            <button
              class="button is-rounded is-light"
              type="submit"
              on:click={del}
            >
              삭제
            </button>
          </div>
        {/if}
      {/if}
      <div style="float:left;">
        <span class="is-size-3">{article.title}</span> <br />
        <div style="float: left;">
          <a
            class="author"
            href="/free/{article.username}"
            style="color: #4A4A4A;">{article.username}</a
          >
          <span style="color: #DBDBDB;">|</span>
          {article.created}
        </div>
      </div>
      <div style="clear:both" />
    </div>
  </header>

  <hr style="margin:0;" />

  <div class="content">{@html article.content}</div>

  <form
    style="margin: 0 auto; width: 100px; text-align: center"
    on:submit|preventDefault={isClicked ? Like : disLike}
  >
    <span class="is-size-3">
      {#if isLogin}
        <i
          class={isClicked ? "fa-solid fa-heart" : "fa-regular fa-heart"}
          on:click={likeclick}
        />
      {:else}
        <i class="fa-regular fa-heart" on:click={alt} />
      {/if}
    </span>
    <div>추천 {article.like}</div>
  </form>
{/await}

<hr style="margin-top: 0;" />

<div class="comment" style="padding: 16px">
  <table class="table container is-fluid">
    <tbody>
      {#await comments then comments}
        {#if comments.list.length === 0}
          <tr>
            <td>댓글이 없습니다.</td>
          </tr>
        {:else}
          {#each comments["list"] as comment}
            <tr>
              <td>
                <a
                  class="author"
                  href="/free/{comment.username}"
                  style="color: #4A4A4A;"
                >
                  {comment.username}
                </a>
                <span style="color: #DBDBDB;">|</span>
                {comment.created}
              </td>
            </tr>
            <tr>
              <td>{comment.content}</td>
            </tr>
            {#if isLogin}
              {#if Number(window.sessionStorage["user.id"]) == comment.userid}
                <button
                  class="button is-rounded
							is-link is-light is-small
							is-responsive
							"
                  on:click={delete_comment(comment.cid)}
                >
                  삭제
                </button>
              {/if}
            {/if}
          {/each}
        {/if}
      {/await}
    </tbody>
  </table>
  {#if isLogin}
    <form method="POST" on:submit|preventDefault={upload}>
      <div class="contents" contenteditable="true">
        <textarea
          class="input"
          bind:value={comment_content}
          placeholder="댓글을 입력하세요"
          required
        />
      </div>
      <button class="button" type="submit">등록</button>
    </form>
  {/if}
</div>
<List />
<br /><br /><br />

<style>
  hr {
    border: 1px solid #dbdbdb;
  }
  span i {
    color: rgb(251, 106, 130);
  }
  .content {
    width: 100%;
    min-height: 300px;
    padding: 16px;
  }
  .comment table {
    width: 100%;
    background-color: rgba(239, 235, 235, 0.805);
  }
</style>
