import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { MaterialModule } from '@angular/material';

import { ArticleComponent } from 'app/comp/article/article.component';

const Routes: Routes = [
    { path: '', component: ArticleComponent },
]

@NgModule({
    imports: [
        CommonModule,
        MaterialModule,
        FormsModule,
        RouterModule.forChild(Routes)
    ],
    declarations: [
        ArticleComponent
    ]
})
export class ArticleModule { }
