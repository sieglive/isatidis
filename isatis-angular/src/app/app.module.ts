import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';

import { AppComponent } from 'app/app.component';

import { MaterialModule } from '@angular/material';
import { HttpModule, JsonpModule } from '@angular/http';
import { FroalaEditorModule, FroalaViewModule } from 'angular-froala-wysiwyg';
import { HighlightJsModule, HighlightJsService } from 'angular2-highlight-js';

import { ConvertFormat } from 'app/pipe/app.pipe';
import { WindowRef } from 'app/service/window.service';
import { IsatisHttp } from 'app/service/isatis_http.service';
import { Scrollor } from 'app/service/scrollor.service';
// import { BackgroundService } from 'app/background.service';

const appRoutes: Routes = [
    { path: '', redirectTo: 'home', pathMatch: 'full' },
    { path: 'auth', loadChildren: 'app/module/user_auth/user_auth.module#UserAuthModule' },
    { path: 'bulletin', loadChildren: 'app/module/bulletin/bulletin.module#BulletinModule' },
    { path: 'home', loadChildren: 'app/module/home/home.module#HomeModule' },
    { path: 'article', loadChildren: 'app/module/article/article.module#ArticleModule' },
    { path: 'profile', loadChildren: 'app/module/profile/profile.module#ProfileModule' },
    { path: 'about', loadChildren: 'app/module/about/about.module#AboutModule' },
    { path: 'editor', loadChildren: 'app/module/editor/editor.module#EditorModule' }
];

@NgModule({
    declarations: [
        AppComponent,
        ConvertFormat
    ],
    imports: [
        FormsModule,
        BrowserModule,
        BrowserAnimationsModule,
        MaterialModule,
        HttpModule,
        JsonpModule,
        HighlightJsModule,
        RouterModule.forRoot(appRoutes)
    ],
    providers: [WindowRef, IsatisHttp, Scrollor, HighlightJsService],
    bootstrap: [AppComponent]
})
export class AppModule { }

