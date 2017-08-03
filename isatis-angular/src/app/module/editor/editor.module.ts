import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { MaterialModule } from '@angular/material';

import { EditorComponent } from './editor.component';

const Routes: Routes = [
    { path: '', component: EditorComponent },
]

@NgModule({
    imports: [
        CommonModule,
        MaterialModule,
        FormsModule,
        RouterModule.forChild(Routes)
    ],
    declarations: [
        EditorComponent
    ]
})
export class EditorModule { }
