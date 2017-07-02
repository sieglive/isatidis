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
import { UserAuthComponent } from 'app/comp/user/user_auth.component'
import { MaterialModule } from '@angular/material';
import { HttpModule, JsonpModule } from '@angular/http';

import { ConvertFormat } from 'app/pipe/app.pipe';
import { WindowRef } from 'app/service/window.service';
import { IsatisHttp } from 'app/service/isatis_http.service';
// import { BackgroundService } from 'app/background.service';

const appRoutes: Routes = [
    { path: '', redirectTo: 'bulletin', pathMatch: 'full' },
    { path: 'auth', component: UserAuthComponent },
    { path: 'bulletin', component: BulletinComponent },
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
        BulletinComponent,
        UserAuthComponent,
        ConvertFormat
    ],
    imports: [
        FormsModule,
        BrowserModule,
        BrowserAnimationsModule,
        MaterialModule,
        HttpModule,
        JsonpModule,
        RouterModule.forRoot(appRoutes)
    ],
    providers: [WindowRef, IsatisHttp],
    bootstrap: [AppComponent]
})
export class AppModule { }

