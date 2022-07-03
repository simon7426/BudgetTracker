describe('Navigation', () => {
  it('Can navigate to login from home.', () => {
      cy.visit('/');
      cy.contains('Login')
      cy.contains('Register').click()
  })
})