import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';


import { AppComponent } from './app.component';
import { HomeComponent } from './comp/home/home.component'
import { ArticleComponent } from './comp/article/article.component';
import { ProfileComponent } from './comp/profile/profile.component';

// import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
const appRoutes: Routes = [
    { path: '', redirectTo: 'home', pathMatch: 'full' },
    { path: 'home', component: HomeComponent },
    { path: 'article', component: ArticleComponent },
    { path: 'profile', component: ProfileComponent },
];

@NgModule({
    declarations: [
        AppComponent,
        HomeComponent,
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
