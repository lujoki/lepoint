;; ---- Emacs Config ----
;;  Luke Kirkpatrick
;;  Last edit: 01/09/10
;; ----------------------
;; Requires
;; 	Fonts: terminus
;;	Addons: color-theme


;; ========= Emacs Look & Feel ==========

(require 'color-theme)
(setq color-theme-is-global t)
(color-theme-calm-forest)
(set-default-font "-*-terminus-medium-r-*-*-16-*-*-*-*-*-*-*")

;; Hide menubar
;;(menu-bar-mode 0)
;; Hide toolbar
(tool-bar-mode 0)

;; ========== Buffer Settings ==========

;; Open file on load
(find-file "~/Dropbox/org/life.org")

(setq default-directory "~/")

;; Turn off welcome help message
(setq inhibit-startup-message t)

;; New buffers treated as org-mode
(setq default-major-mode 'org-mode)

;; Set buffers on per filetype basis
(setq auto-mode-alist
  (append
    '(("\\.org$" . org-mode)
      ("\\.txt$" . text-mode))
    auto-mode-alist))

;; ========== Aliases ==========

;; Type y or n for yes-no
(defalias 'yes-or-no-p 'y-or-n-p)

;; ========== Cursor Settings ==========

;; Stop cursor blinking
(blink-cursor-mode -1)

;; ========== Line & Column Settings ==========

;; Show line-number in the mode line
(line-number-mode 1)

;; Show column-number in the mode line
(column-number-mode 1)

;; Set column wrap width 
(setq-default fill-column 72)

;; ========== Place Backup Files in Specific Directory ==========

;; Enable backup files.
(setq make-backup-files t)

;; Enable versioning with default values (keep five last versions, I think!)
(setq version-control t)

;; Save all backup file in this directory.
(setq backup-directory-alist (quote ((".*" . "~/.emacs_backups/"))))

;; =============== Function to Delete a Line ==========

;; First define a variable which will store the previous column position
(defvar previous-column nil "Save the column position")

;; Define the nuke-line function. The line is killed, then the newline
;; character is deleted. The column which the cursor was positioned at is then
;; restored. Because the kill-line function is used, the contents deleted can
;; be later restored by usibackward-delete-char-untabifyng the yank commands.
(defun nuke-line()
  "Kill an entire line, including the trailing newline character"
  (interactive)

  ;; Store the current column position, so it can later be restored for a more
  ;; natural feel to the deletion
  (setq previous-column (current-column))

  ;; Now move to the end of the current line
  (end-of-line)

  ;; Test the length of the line. If it is 0, there is no need for a
  ;; kill-line. All that happens in this case is that the new-line character
  ;; is deleted.
  (if (= (current-column) 0)
    (delete-char 1)

    ;; This is the 'else' clause. The current line being deleted is not zero
    ;; in length. First remove the line by moving to its start and then
    ;; killing, followed by deletion of the newline character, and then
    ;; finally restoration of the column position.
    (progn
      (beginning-of-line)
      (kill-line)
      (delete-char 1)
      (move-to-column previous-column))))

;; Now bind the delete line function to the F8 key
(global-set-key [f8] 'nuke-line)

;; =============== Function to Insert Todays Date ==========

(defun insert-date (prefix)
    "Insert the current date. With prefix-argument, use ISO format. With
   two prefix arguments, write out the day and month name."
    (interactive "P")
    (let ((format (cond
                   ((not prefix) "%d-%m-%Y")
                   ((equal prefix '(4)) "%Y-%m-%d")
                   ((equal prefix '(16)) "%A, %d. %B %Y")))
          (system-time-locale "en_GB"))
      (insert (format-time-string format))))

(global-set-key (kbd "C-c d") 'insert-date)

;; =============== Bind Switch To Life Buffer ============

(defun life-buffer()
  "Switch to the default org buffer"
  (interactive)
  (switch-to-buffer "life.org"))

(global-set-key (kbd "C-c l") 'life-buffer)

;; ======= Set Window Size Acording to Monitor Res =======

(defun set-frame-size-according-to-resolution ()
  (interactive)
  (if window-system
  (progn
    ;; use 120 char wide window for largeish displays
    ;; and smaller 80 column windows for smaller displays
    ;; pick whatever numbers make sense for you
    (if (> (x-display-pixel-width) 1440)
        (add-to-list 'default-frame-alist (cons 'width 120))
      (add-to-list 'default-frame-alist (cons 'width 100)))
    ;; for the height, subtract a couple hundred pixels
    ;; from the screen height (for panels, menubars and
    ;; whatnot), then divide by the height of a char to
    ;; get the height we want
    (add-to-list 'default-frame-alist 
     (cons 'height (/ (- (x-display-pixel-height) 100) (frame-char-height)))))))

(set-frame-size-according-to-resolution)