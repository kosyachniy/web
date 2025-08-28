'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import { Box } from '@/shared/ui/box';
import { IconButton } from '@/shared/ui/icon-button';
import { ButtonGroup } from '@/shared/ui/button-group';
import { 
  CheckCircleIcon,
  QuestionIcon,
  ThumbsUpIcon,
  ThumbsDownIcon
} from '@/shared/ui/icons';

interface QuestionnaireSidebarProps {
  className?: string;
}

interface Question {
  id: string;
  question: string;
  type: 'rating' | 'yesno' | 'choice';
  options?: string[];
}

export default function QuestionnaireSidebar({ className }: QuestionnaireSidebarProps) {
  const t = useTranslations('questionnaire');
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});

  const questions: Question[] = [
    {
      id: 'satisfaction',
      question: t('howSatisfied'),
      type: 'rating'
    },
    {
      id: 'recommendation',
      question: t('wouldRecommend'),
      type: 'yesno'
    },
    {
      id: 'improvement',
      question: t('whatImprove'),
      type: 'choice',
      options: [t('performance'), t('design'), t('features'), t('content')]
    }
  ];

  const handleAnswer = (questionId: string, answer: string) => {
    setAnswers(prev => ({ ...prev, [questionId]: answer }));
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(prev => prev + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(prev => prev - 1);
    }
  };

  const handleSubmit = () => {
    console.log('Questionnaire submitted:', answers);
    // Reset questionnaire
    setCurrentQuestion(0);
    setAnswers({});
  };

  const currentQ = questions[currentQuestion];
  const isCompleted = Object.keys(answers).length === questions.length;
  const hasCurrentAnswer = answers[currentQ?.id];

  return (
    <Box size="default" className={className}>
      <div className="space-y-4">
        <div className="flex items-center gap-2 mb-4">
          <QuestionIcon size={20} />
          <h3 className="font-semibold text-lg">{t('feedback')}</h3>
        </div>

        {!isCompleted ? (
          <>
            {/* Progress */}
            <div className="space-y-2">
              <div className="flex justify-between text-sm text-muted-foreground">
                <span>{t('question')} {currentQuestion + 1} / {questions.length}</span>
                <span>{Math.round(((currentQuestion + 1) / questions.length) * 100)}%</span>
              </div>
              <div className="w-full bg-muted rounded-full h-2">
                <div 
                  className="bg-primary rounded-full h-2 transition-all"
                  style={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
                />
              </div>
            </div>

            {/* Current Question */}
            <div className="space-y-4">
              <h4 className="font-medium">{currentQ?.question}</h4>

              {/* Rating Type */}
              {currentQ?.type === 'rating' && (
                <div className="flex gap-1">
                  {[1, 2, 3, 4, 5].map((rating) => (
                    <IconButton
                      key={rating}
                      variant={answers[currentQ.id] === rating.toString() ? 'default' : 'outline'}
                      size="sm"
                      onClick={() => handleAnswer(currentQ.id, rating.toString())}
                    >
                      {rating}
                    </IconButton>
                  ))}
                </div>
              )}

              {/* Yes/No Type */}
              {currentQ?.type === 'yesno' && (
                <ButtonGroup>
                  <IconButton
                    icon={<ThumbsUpIcon size={16} />}
                    variant={answers[currentQ.id] === 'yes' ? 'success' : 'outline'}
                    onClick={() => handleAnswer(currentQ.id, 'yes')}
                    responsive
                  >
                    {t('yes')}
                  </IconButton>
                  <IconButton
                    icon={<ThumbsDownIcon size={16} />}
                    variant={answers[currentQ.id] === 'no' ? 'destructive' : 'outline'}
                    onClick={() => handleAnswer(currentQ.id, 'no')}
                    responsive
                  >
                    {t('no')}
                  </IconButton>
                </ButtonGroup>
              )}

              {/* Choice Type */}
              {currentQ?.type === 'choice' && currentQ.options && (
                <div className="space-y-2">
                  {currentQ.options.map((option) => (
                    <IconButton
                      key={option}
                      variant={answers[currentQ.id] === option ? 'default' : 'ghost'}
                      className="w-full justify-start"
                      size="sm"
                      onClick={() => handleAnswer(currentQ.id, option)}
                      responsive
                    >
                      {option}
                    </IconButton>
                  ))}
                </div>
              )}
            </div>

            {/* Navigation */}
            <ButtonGroup className="w-full">
              <IconButton
                variant="outline"
                disabled={currentQuestion === 0}
                onClick={handlePrevious}
                className="flex-1"
              >
                {t('previous')}
              </IconButton>
              <IconButton
                variant="default"
                disabled={!hasCurrentAnswer}
                onClick={currentQuestion === questions.length - 1 ? handleSubmit : handleNext}
                className="flex-1"
              >
                {currentQuestion === questions.length - 1 ? t('submit') : t('next')}
              </IconButton>
            </ButtonGroup>
          </>
        ) : (
          <div className="text-center space-y-4">
            <CheckCircleIcon size={48} className="mx-auto text-green-500" />
            <div>
              <h4 className="font-medium">{t('thankYou')}</h4>
              <p className="text-sm text-muted-foreground">{t('feedbackReceived')}</p>
            </div>
            <IconButton
              variant="outline"
              onClick={() => {
                setCurrentQuestion(0);
                setAnswers({});
              }}
              className="w-full"
            >
              {t('takeAgain')}
            </IconButton>
          </div>
        )}
      </div>
    </Box>
  );
}