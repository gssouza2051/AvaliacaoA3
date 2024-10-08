module.exports = {
    extends: ['@commitlint/config-conventional'],
    rules: {
      'subject-full-stop': [0, 'never'], // Permite ponto final no subject
      'type-enum': [
        2,
        'always',
        ['feat', 'fix', 'docs', 'style', 'refactor', 'perf', 'test', 'build', 'ci', 'chore', 'revert', 'merge']
      ],
      'subject-case': [0, 'never'], // Permite letras maiúsculas e minúsculas
      'body-leading-blank': [1, 'always'],
      'footer-prefix': [1, 'always', ['BREAKING CHANGE', 'Reviewed-by']],
      'subject-empty': [2, 'never'],
      'subject-case': [0, 'never'],
      'subject-max-length': [2, 'always', 72],
      'type-empty': [2, 'never']
    },
    // Adicione a regra para verificar palavras-chave
    customRules: {
      'custom-rule': [
        2,
        'always',
        (commit) => {
          const keywords = ['importante', 'urgente', 'bug']; // Lista de palavras-chave
          return keywords.some((keyword) => commit.message.includes(keyword));
        }
      ]
    }
  };