import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { HomeComponent } from './comp/home/home.component'
import { ArticleComponent } from './comp/article/article.component';
import { ProfileComponent } from './comp/profile/profile.component';
import { AboutComponent } from './comp/about/about.component';
import { MdButtonModule, MdInputModule, MdToolbarModule, MdIconModule, MdCardModule } from '@angular/material';

import { ConvertFormat } from './app.pipe';

const appRoutes: Routes = [
    { path: '', redirectTo: 'home', pathMatch: 'full' },
    { path: 'home', component: HomeComponent },
    { path: 'article', component: ArticleComponent },
    { path: 'profile', component: ProfileComponent },
    { path: 'about', component: AboutComponent },
];

@NgModule({
    declarations: [
        AppComponent,
        HomeComponent,
        ArticleComponent,
        ProfileComponent,
        AboutComponent,
        ConvertFormat
    ],
    imports: [
        FormsModule,
        BrowserModule,
        BrowserAnimationsModule,
        MdButtonModule,
        // MdCheckboxModule,
        MdToolbarModule,
        MdInputModule,
        MdIconModule,
        MdCardModule,
        RouterModule.forRoot(appRoutes)
    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule { }
