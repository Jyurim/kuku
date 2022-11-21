<script>
	import env from "$lib/env.js";

	const async_course_list = fetch(`${env.baseUrl}/study/head-chapters/`, {
		method: "GET",
		headers: {
			Accept: "application/json",
		},
		mode: "cors",
		credentials: "include",
	}).then((resp) => resp.json());
</script>

<div class="container">
	<section class="section has-text-centered header">
		<h1 class="title">배우고 싶은것들을 살펴보세요</h1>
		<h2 class="subtitle mt-1 has-text-grey">
			한 곳에서 각 분야의 알고리즘을 배울 수 있습니다. 배우고 싶은것을
			찾아보세요
		</h2>
	</section>
	<br /><br /><br />
	{#await async_course_list}
		<div class="p-6">
			<progress class="progress is-small is-primary" max="100"
				>Loading in progress</progress
			>
		</div>
	{:then list}
		<div class="columns is-flex-wrap-wrap">
			{#each list as item}
				<div class="column is-one-quarter mb-4">
					<a href="/study/{item.course_slug}/{item.no}">
						<div class="card">
							<header class="card-header">
								<h1
									class="card-header-title has-background-light"
								>
									{item.course_title}
								</h1>
							</header>
							<div class="card-content content">
								<h4 class="subtitle mb-4">{item.title}</h4>
								{#if item.category != ""}
									<span class="tag mr-1 is-dark"
										>{item.category}</span
									>
								{/if}
								{#each item.supported_languages as lang}
									<span class="tag mr-1 is-light">{lang}</span
									>
								{/each}
							</div>
						</div></a
					>
				</div>
			{/each}
		</div>
	{/await}
</div>

<style>
	.section.header {
		line-height: 1.3;
	}
	.container {
		margin-top: 1rem;
		margin-bottom: 2rem;
	}
	.chapter-description {
		height: 3rem;
		max-height: 3rem;
		text-overflow: ellipsis;
		white-space: nowrap;
		overflow: hidden;
	}

	:global(body > div > main) {
		min-height: calc(100vh - 220px);
	}
</style>
