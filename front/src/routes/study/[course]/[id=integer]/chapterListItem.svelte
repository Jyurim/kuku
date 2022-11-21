<script>
	export let item;
	export let course_id;
	export let selected_id;
	export let depth = 0;

	let children = item.children;
</script>

<option value={item.no} selected={selected_id == item.no}>
	{"　".repeat(depth)}{item.title}
</option>
{#each children as child}
	<svelte:self item={child} {course_id} depth={depth + 1} {selected_id} />
{/each}
>
