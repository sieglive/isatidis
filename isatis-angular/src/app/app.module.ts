import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';


import { AppComponent } from './app.component';
import { ArticleComponent } from './comp/article/article.component';
import { ProfileComponent } from './comp/profile/profile.component';

// import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
const appRoutes: Routes = [
    { path: '', redirectTo: 'article', pathMatch: 'full' },
    { path: 'article', component: ArticleComponent },
    { path: 'profile', component: ProfileComponent },
];

@NgModule({
    declarations: [
        AppComponent,
        ArticleComponent,
        ProfileComponent
    ],
    imports: [
        // NgbModule.forRoot(),
        RouterModule.forRoot(appRoutes),
        BrowserModule
    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule { }
