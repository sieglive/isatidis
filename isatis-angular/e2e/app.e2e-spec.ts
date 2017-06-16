import { IsatisPage } from './app.po';

describe('isatis App', () => {
  let page: IsatisPage;

  beforeEach(() => {
    page = new IsatisPage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!!');
  });
});
