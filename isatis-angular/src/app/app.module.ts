import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';

import { AppComponent } from 'app/app.component';
import { HomeComponent } from 'app/comp/home/home.component'
import { ArticleComponent } from 'app/comp/article/article.component';
import { ProfileComponent } from 'app/comp/profile/profile.component';
import { AboutComponent } from 'app/comp/about/about.component';
import { BulletinComponent } from 'app/comp/bulletin/bulletin.component';
import { UserAuthComponent } from 'app/comp/user/user_auth.component';
import { EditorComponent } from 'app/comp/editor/editor.component';
import { MaterialModule } from '@angular/material';
import { HttpModule, JsonpModule } from '@angular/http';
import { FroalaEditorModule, FroalaViewModule } from 'angular-froala-wysiwyg';

import { MarkdownModule } from 'angular2-markdown';
import { ConvertFormat } from 'app/pipe/app.pipe';
import { WindowRef } from 'app/service/window.service';
import { IsatisHttp } from 'app/service/isatis_http.service';
import { Scrollor } from 'app/service/scrollor.service';
// import { BackgroundService } from 'app/background.service';

const appRoutes: Routes = [
    { path: '', redirectTo: 'bulletin', pathMatch: 'full' },
    { path: 'auth', component: UserAuthComponent },
    { path: 'bulletin', component: BulletinComponent },
    { path: 'home', component: HomeComponent, pathMatch: 'full' },
    { path: 'article', component: ArticleComponent },
    { path: 'profile', component: ProfileComponent },
    { path: 'about', component: AboutComponent },
    { path: 'editor', component: EditorComponent }
];

@NgModule({
    declarations: [
        AppComponent,
        HomeComponent,
        ArticleComponent,
        ProfileComponent,
        AboutComponent,
        BulletinComponent,
        UserAuthComponent,
        EditorComponent,
        ConvertFormat
    ],
    imports: [
        FormsModule,
        BrowserModule,
        BrowserAnimationsModule,
        MaterialModule,
        HttpModule,
        JsonpModule,
        MarkdownModule.forRoot(),
        FroalaEditorModule.forRoot(),
        FroalaViewModule.forRoot(),
        RouterModule.forRoot(appRoutes)
    ],
    providers: [WindowRef, IsatisHttp, Scrollor],
    bootstrap: [AppComponent]
})
export class AppModule { }

