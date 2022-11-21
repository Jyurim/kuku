<script>
	import { is_empty } from "svelte/internal";

	let username = "",
		email = "",
		password = "",
		confirmpassword = "";

	let valid_email =
		/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	let show_password = false;
	let show_confirmpassword = false;
	function passwordShow_button() {
		show_password = !show_password;
	}
	function confirmpasswordShow_button() {
		show_confirmpassword = !show_confirmpassword;
	}
	let passwordThis;
	let confirmpasswordThis;
	let usernameFailed = true;
	let usernameExcepts = ["ㅅㅂ", "kuku"];

	/**checking user name is available
	이후 제한 사항들을 추가해야 합니다.
	*/
	const filterUsername = () => {
		if (is_empty(username)) {
			return false;
		} else if (
			usernameExcepts.filter((e) => {
				return username.includes(e);
			}).length > 0
		) {
			return false;
		} else {
			return true;
		}
	};

	const check_username = async () =>
		await fetch(`//api.eyo.kr:8081/user/check?username=${username}`, {
			method: "GET",
			headers: {
				Aceept: "application/json",
			},
			mode: "cors",
			credentials: "include",
		})
			.then((res) => {
				if (res.ok) return res.json();
			})
			.then((data) => {
				if (data === true) {
					usernameFailed = false;
					isLoading = false;
				} else {
					usernameFailed = true;
					isLoading = false;
				}
			})
			.catch((err) => {
				console.log(err);
			});

	const checkUsername = () => {
		isLoading = true;
		if (filterUsername()) {
			check_username();
		} else {
			usernameFailed = true;
			isLoading = false;
		}
	};

	let isLoading = false;
	let message = "";

	const postUser = async () => {
		isLoading = true;

		await fetch("//api.eyo.kr:8081/user/user", {
			method: "POST",
			headers: {
				Aceept: "application/json",
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				username,
				password,
				email,
			}),
			mode: "cors",
			credentials: "include",
		})
			.then((res) => {
				if (res.ok == false) return Promise.reject(res);
				return res.json();
			})
			.then(() => {
				location.href = "?msg=회원가입 되었습니다. 로그인 해주세요.";
				isLoading = false;
			})
			.catch((e) => {
				e.json().then((json) => {
					message = "회원가입에 실패하였습니다: " + json["detail"];
					isLoading = false;
				});
			});
	};
</script>

<form method="post" on:submit|preventDefault={postUser}>
	{#if message != ""}
		<article class="message is-danger">
			<div class="message-body">
				{message}
			</div>
		</article>
	{/if}
	<div class="field">
		<label class="label" for="username">Username</label>
		<div class="control has-icons-left has-icons-right">
			<input
				class="input"
				class:is-danger={usernameFailed && !is_empty(username)}
				class:is-success={!usernameFailed}
				name="username"
				type="text"
				placeholder="Set your new username"
				bind:value={username}
				on:input={checkUsername}
				required
			/>
			<span class="icon is-small is-left ">
				<i
					class="fa-regular fa-user"
					class:has-text-danger={usernameFailed &&
						!is_empty(username)}
					class:has-text-success={!usernameFailed}
				/>
			</span>
			{#if isLoading}
				<span class="icon fa-sm is-right ">
					<i
						class="fa-solid fa-circle-notch fa-spin"
						class:has-text-danger={usernameFailed &&
							!is_empty(username)}
						class:has-text-success={!usernameFailed}
					/>
				</span>
			{:else}
				<span class="icon is-small is-right">
					<i
						class="fas fa-check"
						class:has-text-danger={usernameFailed &&
							!is_empty(username)}
						class:has-text-success={!usernameFailed}
					/>
				</span>

				{#if usernameFailed && !is_empty(username)}<p
						class="help has-text-danger"
					>
						{username} is not available
					</p>{/if}
			{/if}
		</div>
		<p class="help">Write your name to be shown to others</p>
	</div>
	<div class="field">
		<label class="label" for="email">Email</label>
		<div class="control has-icons-left has-icons-right">
			<input
				class="input"
				class:is-danger={!email.match(valid_email) && !is_empty(email)}
				class:is-success={email.match(valid_email)}
				name="email"
				type="text"
				placeholder="Set your new email"
				bind:value={email}
				required
			/>
			<span class="icon is-small is-left">
				<i
					class="fa-regular fa-envelope"
					class:has-text-danger={!email.match(valid_email) &&
						!is_empty(email)}
					class:has-text-success={email.match(valid_email)}
				/>
			</span>
			<span class="icon is-small is-right">
				<i
					class="fas fa-check"
					class:has-text-danger={!email.match(valid_email) &&
						!is_empty(email)}
					class:has-text-success={email.match(valid_email)}
				/>
			</span>
		</div>
		<p class="help">Write your email</p>
	</div>

	<div class="field">
		<label class="label" for="password">Password</label>
		<div class="control has-icons-left has-icons-right">
			<div class="control">
				<input
					class="input"
					class:is-danger={(!is_empty(password) &&
						password.length < 8) ||
						password.length > 128}
					class:is-success={password.length > 7 &&
						password.length < 129}
					name="password"
					type={show_password ? "text" : "password"}
					placeholder="Set your new password"
					bind:this={passwordThis}
					on:input={() => (password = passwordThis.value)}
					required
				/>
				<span class="icon is-small is-left">
					<i
						class="fas fa-key"
						class:has-text-danger={(!is_empty(password) &&
							password.length < 8) ||
							password.length > 128}
						class:has-text-success={password.length > 7 &&
							password.length < 129}
					/>
				</span>
				<span class="icon is-small is-right">
					<i
						class={show_password
							? "fas fa-eye password_icon"
							: "fas fa-eye-slash password_icon"}
						on:click={passwordShow_button}
						class:has-text-danger={(!is_empty(password) &&
							password.length < 8) ||
							password.length > 128}
						class:has-text-success={password.length > 7 &&
							password.length < 129}
					/>
				</span>
			</div>
		</div>
		<p class="help">Should contain at least 8 ~ 128 characters</p>
	</div>

	<div class="field">
		<label class="label" for="confirmpassword">Confirm Password</label>
		<div class="control has-icons-left has-icons-right">
			<input
				class="input"
				class:is-danger={!is_empty(confirmpassword) &&
					password !== confirmpassword}
				class:is-success={password === confirmpassword &&
					password.length > 7 &&
					password.length < 129}
				name="confirmpassword"
				type={show_confirmpassword ? "text" : "password"}
				placeholder="Confirm your new password"
				bind:this={confirmpasswordThis}
				on:input={() => (confirmpassword = confirmpasswordThis.value)}
				required
			/>
			<span class="icon is-small is-left">
				<i
					class="fas fa-key"
					class:has-text-danger={!is_empty(confirmpassword) &&
						password !== confirmpassword}
					class:has-text-success={password === confirmpassword &&
						password.length > 7 &&
						password.length < 129}
				/>
			</span>
			<span class="icon is-small is-right">
				<i
					class={show_confirmpassword
						? "fas fa-eye confirmpassword_icon"
						: "fas fa-eye-slash confirmpassword_icon"}
					on:click={confirmpasswordShow_button}
					class:has-text-danger={!is_empty(confirmpassword) &&
						password !== confirmpassword}
					class:has-text-success={password === confirmpassword &&
						password.length > 7 &&
						password.length < 129}
				/>
			</span>
		</div>
	</div>

	<div class="field is-grouped">
		<div class="control">
			<button
				class="button is-link"
				class:is-loading={isLoading}
				disabled={isLoading}
				type="submit">Signup</button
			>
		</div>
		<div class="control">
			<button class="button is-link is-light" type="button">Cancel</button
			>
		</div>
	</div>
</form>

<style>
	.password_icon {
		pointer-events: all;
		cursor: pointer;
	}
	.confirmpassword_icon {
		pointer-events: all;
		cursor: pointer;
	}
</style>
