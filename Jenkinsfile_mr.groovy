#!groovy

def handleCheckout = {
	if (env.gitlabMergeRequestId) {
		sh "echo 'Merge request detected. Merging...'"
		def credentialsId = scm.userRemoteConfigs[0].credentialsId
		checkout ([
			$class: 'GitSCM',
			branches: [[name: "${env.gitlabSourceNamespace}/${env.gitlabSourceBranch}"]],
			extensions: [
				[$class: 'PruneStaleBranch'],
				[$class: 'CleanCheckout'],
				[
					$class: 'PreBuildMerge',
					options: [
						fastForwardMode: 'NO_FF',
						mergeRemote: env.gitlabTargetNamespace,
						mergeTarget: env.gitlabTargetBranch
					]
				]
			],
			userRemoteConfigs: [
				[
					credentialsId: credentialsId,
					name: env.gitlabTargetNamespace,
					url: env.gitlabTargetRepoSshURL
				],
				[
					credentialsId: credentialsId,
					name: env.gitlabSourceNamespace,
					url: env.gitlabSourceRepoSshURL
				]
			]
		])
	} else {
		sh "echo 'No merge request detected. Checking out current branch'"
		checkout ([
			$class: 'GitSCM',
			branches: scm.branches,
			extensions: [
					[$class: 'PruneStaleBranch'],
					[$class: 'CleanCheckout']
			],
			userRemoteConfigs: scm.userRemoteConfigs
		])
	}
}

node() {
	stage('setup') {
		sh "env | sort"
		handleCheckout()
		sh "git branch -vv"
	}

	stage('test') {
		sh "echo 'Throw in some tests here'"