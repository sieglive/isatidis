import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';


import { AppComponent } from './app.component';
import { HomeComponent } from './comp/home/home.component'
import { ArticleComponent } from './comp/article/article.component';
import { ProfileComponent } from './comp/profile/profile.component';
import { MdButtonModule, MdInputModule, MdToolbarModule } from '@angular/material';
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

        BrowserModule,
        BrowserAnimationsModule,
        MdButtonModule,
        // MdCheckboxModule,
        MdToolbarModule,
        MdInputModule,
        RouterModule.forRoot(appRoutes)
    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule { }
